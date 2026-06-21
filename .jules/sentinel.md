## 2024-06-21 - EncryptedSerializer Downgrade and Assert Bypass
**Vulnerability:** `EncryptedSerializer` allowed unencrypted data fallback, and `PycryptodomeAesCipher` used `assert` for validation which is bypassed in optimized mode (`-O`).
**Learning:** Security validation must never rely on `assert` statements in Python. Additionally, while downgrade fallbacks are risky, disabling them by default on persistent state serializers (like LangGraph checkpoints) causes major breaking regressions for existing data.
**Prevention:** Use `if not condition: raise ValueError(...)` for security checks. Make unencrypted fallbacks explicitly configurable, but balance default values against backwards compatibility for persistent state.
