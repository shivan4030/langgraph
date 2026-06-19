import pickle
import io
import warnings

class _RestrictedUnpickler(pickle.Unpickler):
    def __init__(self, file, allowed_modules, **kwargs):
        super().__init__(file, **kwargs)
        self.allowed_modules = allowed_modules

    def find_class(self, module, name):
        if self.allowed_modules is True:
            warnings.warn(
                f"Unpickling {module}.{name} in unrestricted mode. "
                "This is a security risk if the checkpoint data is untrusted.",
                UserWarning,
                stacklevel=2,
            )
            return super().find_class(module, name)

        if self.allowed_modules is not None:
            module_parts = tuple(module.split("."))
            for i in range(len(module_parts), 0, -1):
                if module_parts[:i] in self.allowed_modules:
                    return super().find_class(module, name)
            if (module, name) in self.allowed_modules:
                return super().find_class(module, name)

        raise pickle.UnpicklingError(f"Global '{module}.{name}' is forbidden")

print(_RestrictedUnpickler(io.BytesIO(pickle.dumps(set([1, 2, 3]))), allowed_modules={('builtins', 'set')}).load())
print(_RestrictedUnpickler(io.BytesIO(pickle.dumps(set([1, 2, 3]))), allowed_modules={('builtins',)}).load())
try:
    print(_RestrictedUnpickler(io.BytesIO(pickle.dumps(set([1, 2, 3]))), allowed_modules={('os',)}).load())
except Exception as e:
    print(e)
