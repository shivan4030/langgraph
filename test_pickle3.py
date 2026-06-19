import pickle
import io

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        raise pickle.UnpicklingError(f"Global '{module}.{name}' is forbidden")

RestrictedUnpickler(io.BytesIO(pickle.dumps(set([1, 2, 3])))).load()
