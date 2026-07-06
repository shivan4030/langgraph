

## YYYY-MM-DD - Cross-Origin Redirect Header Leakage in SDK
**Vulnerability:** Sensitive headers (like `x-api-key`) were leaked during cross-origin redirects because manual `Location` header following for HTTP streams and reconnects in `libs/sdk-py` bypassed `httpx`'s built-in header stripping.
**Learning:** Manual redirect handling must explicitly reimplement security features like origin comparison and header sanitization.
**Prevention:** Always use `is_cross_origin` and `strip_sensitive_headers` when manually following HTTP redirects.
