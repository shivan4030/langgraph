## 2024-05-15 - Cross-Origin Header Leakage in SDK
**Vulnerability:** Sensitive headers (x-api-key, authorization, cookie) were being forwarded to external domains when HTTP streams or reconnects followed a Location header cross-origin.
**Learning:** `httpx`'s built-in cross-origin header stripping is bypassed because HTTP streaming and reconnects in `libs/sdk-py` manually follow `Location` headers.
**Prevention:** Sensitive headers must be manually stripped when following redirects cross-origin by checking scheme and netloc.
