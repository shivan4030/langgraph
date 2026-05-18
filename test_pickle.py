import io
import pickle
from typing import Any, Literal

class _RestrictedUnpickler(pickle.Unpickler):
    def __init__(
        self,
        file: Any,
        *,
        allowed_modules: set[tuple[str, ...]] | Literal[True] | None,
        **kwargs: Any,
    ) -> None:
        super().__init__(file, **kwargs)
        self.allowed_modules = allowed_modules

    def find_class(self, module: str, name: str) -> Any:
        if self.allowed_modules is True:
            return super().find_class(module, name)
        if self.allowed_modules is not None and (module, name) in self.allowed_modules:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Global '{module}.{name}' is forbidden")

data = pickle.dumps({"a": 1})
unpickler = _RestrictedUnpickler(io.BytesIO(data), allowed_modules={("builtins", "dict")})
try:
    print(unpickler.load())
except Exception as e:
    print("Error:", e)
