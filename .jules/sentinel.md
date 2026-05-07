
## 2026-03-31 - [T9 SDK API Key Leak via Location Redirect]
**Vulnerability:** SDK `HttpClient.request_reconnect()` and `HttpClient.stream()` forward the full `request_headers` dict, including the `x-api-key` authentication header, when following server-provided `Location` redirects. This occurs when connected to a compromised or attacker-controlled LangGraph Server, allowing the key to leak to arbitrary URLs.
**Learning:** The previous HTTP client implementation naively re-applied the original request headers (or a slightly filtered set) without considering the security implications of forwarding authentication tokens to different domains specified by the server.
**Prevention:** Filter out sensitive headers, specifically `x-api-key`, from the `headers` dictionary before passing it into subsequent redirection requests.
