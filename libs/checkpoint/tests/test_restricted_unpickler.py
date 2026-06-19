import os
import pickle

import pytest

from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer


def test_restricted_unpickler():
    serializer = JsonPlusSerializer(pickle_fallback=True)

    # Create malicious payload
    class Malicious:
        def __reduce__(self):
            return (os.system, ("echo hacked",))

    payload = pickle.dumps(Malicious())

    with pytest.raises(pickle.UnpicklingError):
        serializer.loads_typed(("pickle", payload))

    # Test allowed
    import datetime

    payload2 = pickle.dumps(datetime.datetime.now())
    res = serializer.loads_typed(("pickle", payload2))
    assert isinstance(res, datetime.datetime)

    # Test True
    import pandas as pd

    serializer = JsonPlusSerializer(pickle_fallback=True, allowed_pickle_modules=True)
    res = serializer.loads_typed(("pickle", pickle.dumps(pd.DataFrame({"a": [1]}))))
    assert isinstance(res, pd.DataFrame)
