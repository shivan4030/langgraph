## YYYY-MM-DD - Cross-Origin Redirect Header Leakage in SDK
**Vulnerability:** Sensitive headers were leaked during cross-origin redirects because manual `Location` header following for SSE reconnects bypassed `httpx`'s built-in header stripping.
**Learning:** Manual redirect handling must explicitly reimplement security features like origin comparison and header sanitization.
**Prevention:** Always use `is_cross_origin` and `strip_sensitive_headers` when manually following HTTP redirects.
