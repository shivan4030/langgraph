import pickle
import io
from typing import Literal

class _RestrictedUnpickler(pickle.Unpickler):
    def __init__(self, *args, allowed_modules: set[tuple[str, ...]] | Literal[True], **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_modules = allowed_modules

    def find_class(self, module: str, name: str):
        if self.allowed_modules is True:
            return super().find_class(module, name)

        parts = tuple(module.split("."))
        for i in range(1, len(parts) + 1):
            if parts[:i] in self.allowed_modules:
                return super().find_class(module, name)

        raise pickle.UnpicklingError(f"Global '{module}.{name}' is forbidden")

import os
data = pickle.dumps(os.system)
print(data)

unpickler = _RestrictedUnpickler(io.BytesIO(data), allowed_modules={("os",)})
print(unpickler.load())

try:
    unpickler2 = _RestrictedUnpickler(io.BytesIO(data), allowed_modules={("app",)})
    unpickler2.load()
except Exception as e:
    print("Caught:", e)
