import pickle
import io

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        raise pickle.UnpicklingError(f"Global '{module}.{name}' is forbidden")

try:
    RestrictedUnpickler(io.BytesIO(pickle.dumps(set([1, 2, 3])))).load()
except Exception as e:
    print(e)
