## 2025-02-14 - Fix Insecure Deserialization in PersistentDict

**Vulnerability:** Arbitrary Code Execution via Insecure Deserialization in `PersistentDict.load` (`libs/checkpoint/langgraph/checkpoint/memory/__init__.py`).
**Learning:** `PersistentDict` is used as the backing storage for `InMemorySaver` when a `filename` is provided. It blindly used `pickle.load()` to load file contents from disk. Even though a warning exists for `JsonPlusSerializer`, `PersistentDict` is a more foundational persistence layer that doesn't need to deserialize complex user objects (it stores primitives and serialized bytes/strings from `JsonPlusSerializer`).
**Prevention:** Implement a restricted `_SafeUnpickler` inheriting from `pickle.Unpickler` that only allows fundamental Python types (`dict`, `list`, `str`, `bytes`, `_codecs.encode`, etc.) and replace blind `pickle.load()` calls with it in foundational persistence mechanisms.
