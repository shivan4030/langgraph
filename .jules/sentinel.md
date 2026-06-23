## YYYY-MM-DD - Dockerfile ENV Single-Quote Injection
**Vulnerability:** Shell command injection via unescaped single quotes in `langgraph.json` configuration values during Dockerfile generation.
**Learning:** `json.dumps()` does not escape single quotes. When embedded in single-quoted `ENV` or `RUN` directives (e.g., `ENV VAR='{json}'`), it allows premature string termination.
**Prevention:** Always pass serialized JSON through a sanitizer (e.g., `.replace("'", r"'\''")`) before embedding it into shell-evaluated contexts.

## YYYY-MM-DD - Cross-Origin Redirect Header Leakage in SDK
**Vulnerability:** Sensitive headers were leaked during cross-origin redirects because manual `Location` header following for SSE reconnects bypassed `httpx`'s built-in header stripping.
**Learning:** Manual redirect handling must explicitly reimplement security features like origin comparison and header sanitization.
**Prevention:** Always use `is_cross_origin` and `strip_sensitive_headers` when manually following HTTP redirects.

## YYYY-MM-DD - EncryptedSerializer Downgrade and Assert Bypass
**Vulnerability:** `EncryptedSerializer` allowed unencrypted data fallback, and `PycryptodomeAesCipher` used `assert` for validation which is bypassed in optimized mode (`-O`).
**Learning:** Security validation must never rely on `assert` statements in Python. Additionally, while downgrade fallbacks are risky, disabling them by default on persistent state serializers (like LangGraph checkpoints) causes major breaking regressions for existing data.
**Prevention:** Use `if not condition: raise ValueError(...)` for security checks. Make unencrypted fallbacks explicitly configurable, but balance default values against backwards compatibility for persistent state.

## YYYY-MM-DD - Deserialization Warning Log Spam
**Vulnerability:** Placing a backwards-compatibility security warning inside `_RestrictedUnpickler.__init__` caused log spam on every deserialization event.
**Learning:** When a deserializer is instantiated repeatedly (e.g., per payload), warnings should be logged at the configuration level (`JsonPlusSerializer.__init__`) rather than the execution level.
**Prevention:** Emitting configuration-related security warnings during class initialization rather than per-operation execution prevents excessive log noise.

## YYYY-MM-DD - Missing Restricted Unpickler in JsonPlusSerializer
**Vulnerability:** Arbitrary code execution via `pickle.loads` in `JsonPlusSerializer` when `pickle_fallback` is enabled.
**Learning:** The intended `_RestrictedUnpickler` was initially missing but has since been implemented. Fixing it required defaulting the allowlist to `True` (unrestricted) with a `UserWarning` to prevent breaking existing user integrations (e.g., pandas DataFrames).
**Prevention:** Always verify security controls are actively enforced. Use warnings when retroactive security enforcement could break backwards compatibility.
