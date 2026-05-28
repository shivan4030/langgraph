
## 2024-05-28 - Cross-Origin Redirect Header Leakage in SDK
**Vulnerability:** Sensitive headers (like x-api-key, authorization, cookie) were leaked during cross-origin redirects because manual `Location` header following for SSE reconnects bypassed `httpx`'s built-in header stripping logic.
**Learning:** Manual redirect handling must explicitly reimplement security features like origin comparison and header sanitization.
**Prevention:** Always use custom cross-origin verification (`is_cross_origin`) and header sanitization (`strip_sensitive_headers`) when manually following HTTP redirects.
