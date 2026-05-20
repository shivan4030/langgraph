## 2024-05-20 - Missing Restricted Unpickler in JsonPlusSerializer
**Vulnerability:** Arbitrary code execution via `pickle.loads` in `JsonPlusSerializer` when `pickle_fallback` is enabled.
**Learning:** A surprising gap where the intended `_RestrictedUnpickler` was documented but not actually implemented in the codebase.
**Prevention:** Always verify that security controls (like deserialization allowlists) are not just documented but actively enforced in the fallback logic.
