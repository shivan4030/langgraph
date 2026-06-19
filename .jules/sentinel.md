## YYYY-MM-DD - Missing Restricted Unpickler in JsonPlusSerializer
**Vulnerability:** Arbitrary code execution via `pickle.loads` in `JsonPlusSerializer` when `pickle_fallback` is enabled.
**Learning:** The intended `_RestrictedUnpickler` was documented but not implemented. Fixing it required defaulting the allowlist to `True` (unrestricted) with a `UserWarning` to prevent breaking existing user integrations (e.g., pandas DataFrames).
**Prevention:** Always verify security controls are actively enforced. Use warnings when retroactive security enforcement could break backwards compatibility. Ensure exact string comparisons are used properly when attempting to allowlist specific modules or prefixes.
