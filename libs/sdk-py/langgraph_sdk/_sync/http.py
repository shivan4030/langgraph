"""Synchronous HTTP client for LangGraph API."""

from __future__ import annotations

import logging
import sys
import warnings
from collections.abc import Callable, Iterator, Mapping
from typing import Any, cast
from urllib.parse import urlparse

import httpx
import orjson

from langgraph_sdk._shared.utilities import _orjson_default
from langgraph_sdk.errors import _raise_for_status_typed
from langgraph_sdk.schema import QueryParamTypes, StreamPart
from langgraph_sdk.sse import SSEDecoder, iter_lines_raw

logger = logging.getLogger(__name__)


class SyncHttpClient:
    """Handle synchronous requests to the LangGraph API.

    Provides error messaging and content handling enhancements above the
    underlying httpx client, mirroring the interface of [HttpClient](#HttpClient)
    but for sync usage.

    Attributes:
        client (httpx.Client): Underlying HTTPX sync client.
    """

    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    def get(
        self,
        path: str,
        *,
        params: QueryParamTypes | None = None,
        headers: Mapping[str, str] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ) -> Any:
        """Send a `GET` request."""
        r = self.client.get(path, params=params, headers=headers)
        if on_response:
            on_response(r)
        _raise_for_status_typed(r)
        return _decode_json(r)

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | list | None,
        params: QueryParamTypes | None = None,
        headers: Mapping[str, str] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ) -> Any:
        """Send a `POST` request."""
        if json is not None:
            request_headers, content = _encode_json(json)
        else:
            request_headers, content = {}, b""
        if headers:
            request_headers.update(headers)
        r = self.client.post(
            path, headers=request_headers, content=content, params=params
        )
        if on_response:
            on_response(r)
        _raise_for_status_typed(r)
        return _decode_json(r)

    def put(
        self,
        path: str,
        *,
        json: dict,
        params: QueryParamTypes | None = None,
        headers: Mapping[str, str] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ) -> Any:
        """Send a `PUT` request."""
        request_headers, content = _encode_json(json)
        if headers:
            request_headers.update(headers)

        r = self.client.put(
            path, headers=request_headers, content=content, params=params
        )
        if on_response:
            on_response(r)
        _raise_for_status_typed(r)
        return _decode_json(r)

    def patch(
        self,
        path: str,
        *,
        json: dict,
        params: QueryParamTypes | None = None,
        headers: Mapping[str, str] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ) -> Any:
        """Send a `PATCH` request."""
        request_headers, content = _encode_json(json)
        if headers:
            request_headers.update(headers)
        r = self.client.patch(
            path, headers=request_headers, content=content, params=params
        )
        if on_response:
            on_response(r)
        _raise_for_status_typed(r)
        return _decode_json(r)

    def delete(
        self,
        path: str,
        *,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: Mapping[str, str] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ) -> None:
        """Send a `DELETE` request."""
        r = self.client.request(
            "DELETE", path, json=json, params=params, headers=headers
        )
        if on_response:
            on_response(r)
        _raise_for_status_typed(r)

    def request_reconnect(
        self,
        path: str,
        method: str,
        *,
        json: dict[str, Any] | None = None,
        params: QueryParamTypes | None = None,
        headers: Mapping[str, str] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
        reconnect_limit: int = 5,
    ) -> Any:
        """Send a request that automatically reconnects to Location header."""
        request_headers, content = _encode_json(json)
        if headers:
            request_headers.update(headers)
        with self.client.stream(
            method, path, headers=request_headers, content=content, params=params
        ) as r:
            if on_response:
                on_response(r)
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                body = r.read().decode()
                if sys.version_info >= (3, 11):
                    e.add_note(body)
                else:
                    logger.error(f"Error from langgraph-api: {body}", exc_info=e)
                raise e
            loc = r.headers.get("location")
            if reconnect_limit <= 0 or not loc:
                return _decode_json(r)
            try:
                return _decode_json(r)
            except httpx.HTTPError:
                warnings.warn(
                    f"Request failed, attempting reconnect to Location: {loc}",
                    stacklevel=2,
                )
                r.close()
                loc_parsed = urlparse(loc)
                base_parsed = urlparse(str(self.client.base_url))
                is_cross_origin = loc_parsed.netloc != "" and (
                    loc_parsed.netloc != base_parsed.netloc
                    or loc_parsed.scheme != base_parsed.scheme
                )
                reconnect_headers = {
                    k: v
                    for k, v in request_headers.items()
                    if not (is_cross_origin and k.lower() == "x-api-key")
                }
                return self.request_reconnect(
                    loc,
                    "GET",
                    headers=reconnect_headers,
                    # don't pass on_response so it's only called once
                    reconnect_limit=reconnect_limit - 1,
                )

    def stream(
        self,
        path: str,
        method: str,
        *,
        json: dict[str, Any] | None = None,
        params: QueryParamTypes | None = None,
        headers: Mapping[str, str] | None = None,
        on_response: Callable[[httpx.Response], None] | None = None,
    ) -> Iterator[StreamPart]:
        """Stream the results of a request using SSE."""
        if json is not None:
            request_headers, content = _encode_json(json)
        else:
            request_headers, content = {}, None
        request_headers["Accept"] = "text/event-stream"
        request_headers["Cache-Control"] = "no-store"
        if headers:
            request_headers.update(headers)

        last_event_id: str | None = None
        reconnect_path: str | None = None
        reconnect_attempts = 0
        max_reconnect_attempts = 5

        while True:
            is_cross_origin = False
            if reconnect_path is not None:
                loc_parsed = urlparse(reconnect_path)
                base_parsed = urlparse(str(self.client.base_url))
                is_cross_origin = loc_parsed.netloc != "" and (
                    loc_parsed.netloc != base_parsed.netloc
                    or loc_parsed.scheme != base_parsed.scheme
                )

            reconnect_headers = {
                key: value
                for key, value in request_headers.items()
                if key.lower() not in {"content-length", "content-type"}
                and not (is_cross_origin and key.lower() == "x-api-key")
            }

            current_headers = dict(
                request_headers if reconnect_path is None else reconnect_headers
            )
            if last_event_id is not None:
                current_headers["Last-Event-ID"] = last_event_id

            current_method = method if reconnect_path is None else "GET"
            current_content = content if reconnect_path is None else None
            current_params = params if reconnect_path is None else None

            retry = False
            with self.client.stream(
                current_method,
                reconnect_path or path,
                headers=current_headers,
                content=current_content,
                params=current_params,
            ) as res:
                if reconnect_path is None and on_response:
                    on_response(res)
                # check status
                _raise_for_status_typed(res)
                # check content type
                content_type = res.headers.get("content-type", "").partition(";")[0]
                if "text/event-stream" not in content_type:
                    raise httpx.TransportError(
                        "Expected response header Content-Type to contain 'text/event-stream', "
                        f"got {content_type!r}"
                    )

                reconnect_location = res.headers.get("location")
                if reconnect_location:
                    reconnect_path = reconnect_location

                decoder = SSEDecoder()
                try:
                    for line in iter_lines_raw(res):
                        sse = decoder.decode(cast(bytes, line).rstrip(b"\n"))
                        if sse is not None:
                            if decoder.last_event_id is not None:
                                last_event_id = decoder.last_event_id
                            if sse.event or sse.data is not None:
                                yield sse
                except httpx.HTTPError:
                    # httpx.TransportError inherits from HTTPError, so transient
                    # disconnects during streaming land here.
                    if reconnect_path is None:
                        raise
                    retry = True
                else:
                    if sse := decoder.decode(b""):
                        if decoder.last_event_id is not None:
                            last_event_id = decoder.last_event_id
                        if sse.event or sse.data is not None:
                            # See async stream implementation for rationale on
                            # skipping empty flush events.
                            yield sse
            if retry:
                reconnect_attempts += 1
                if reconnect_attempts > max_reconnect_attempts:
                    raise httpx.TransportError(
                        "Exceeded maximum SSE reconnection attempts"
                    )
                continue
            break


def _encode_json(json: Any) -> tuple[dict[str, str], bytes]:
    body = orjson.dumps(
        json,
        _orjson_default,
        orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS,
    )
    content_length = str(len(body))
    content_type = "application/json"
    headers = {"Content-Length": content_length, "Content-Type": content_type}
    return headers, body


def _decode_json(r: httpx.Response) -> Any:
    body = r.read()
    return orjson.loads(body) if body else None
