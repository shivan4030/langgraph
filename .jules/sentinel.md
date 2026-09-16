## YYYY-MM-DD - Missing Restricted Unpickler in JsonPlusSerializer
**Vulnerability:** Arbitrary code execution via `pickle.loads` in `JsonPlusSerializer` when `pickle_fallback` is enabled.
**Learning:** The intended `_RestrictedUnpickler` was initially missing but has since been implemented. Fixing it required defaulting the allowlist to `True` (unrestricted) with a `UserWarning` to prevent breaking existing user integrations (e.g., pandas DataFrames).
**Prevention:** Always verify security controls are actively enforced. Use warnings when retroactive security enforcement could break backwards compatibility.

## YYYY-MM-DD - Deserialization Warning Log Spam
**Vulnerability:** Placing a backwards-compatibility security warning inside `_RestrictedUnpickler.__init__` caused log spam on every deserialization event.
**Learning:** When a deserializer is instantiated repeatedly (e.g., per payload), warnings should be logged at the configuration level (`JsonPlusSerializer.__init__`) rather than the execution level.
**Prevention:** Emitting configuration-related security warnings during class initialization rather than per-operation execution prevents excessive log noise.
