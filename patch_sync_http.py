import re

with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "r") as f:
    content = f.read()

import_statement = "from langgraph_sdk._shared.utilities import (\n    NOT_PROVIDED,\n    _get_headers,\n    _sse_to_v2_dict,\n    configure_loopback_transports,\n    get_asgi_transport,\n    is_cross_origin,\n    strip_sensitive_headers,\n)"

content = re.sub(
    r"from langgraph_sdk\._shared\.utilities import \(\n(?: {4}[^\n]+\n)+\)",
    import_statement,
    content
)

reconnect_replacement = """                r.close()
                next_headers = request_headers.copy()
                if is_cross_origin(str(r.url), loc):
                    next_headers = strip_sensitive_headers(next_headers)

                return self.request_reconnect(
                    loc,
                    "GET",
                    headers=next_headers,
                    # don't pass on_response so it's only called once
                    reconnect_limit=reconnect_limit - 1,
                )"""

content = re.sub(
    r"                r\.close\(\)\n                return self\.request_reconnect\(\n                    loc,\n                    \"GET\",\n                    headers=request_headers,\n                    # don't pass on_response so it's only called once\n                    reconnect_limit=reconnect_limit - 1,\n                \)",
    reconnect_replacement,
    content
)

stream_replacement = """                    if reconnect_limit <= 0 or not loc:
                        break

                    next_headers = request_headers.copy()
                    if is_cross_origin(str(r.url), loc):
                        next_headers = strip_sensitive_headers(next_headers)

                    warnings.warn(
                        f"Stream failed, attempting reconnect to Location: {loc}",
                        stacklevel=2,
                    )
                    yield from self.stream(
                        loc,
                        "GET",
                        headers=next_headers,
                        # don't pass on_response so it's only called once
                        reconnect_limit=reconnect_limit - 1,
                    )"""

content = re.sub(
    r"                    if reconnect_limit <= 0 or not loc:\n                        break\n                    warnings\.warn\(\n                        f\"Stream failed, attempting reconnect to Location: \{loc\}\",\n                        stacklevel=2,\n                    \)\n                    yield from self\.stream\(\n                        loc,\n                        \"GET\",\n                        headers=request_headers,\n                        # don't pass on_response so it's only called once\n                        reconnect_limit=reconnect_limit - 1,\n                    \)",
    stream_replacement,
    content
)

with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "w") as f:
    f.write(content)
