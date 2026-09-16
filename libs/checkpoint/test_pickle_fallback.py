import pytest
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

def test_jsonplus_pickle_fallback():
    serializer = JsonPlusSerializer(pickle_fallback=True)
    pass
