with open("libs/sdk-py/langgraph_sdk/_async/http.py", "r") as f:
    content = f.read()

if "is_cross_origin" not in content:
    content = content.replace("from langgraph_sdk._shared.utilities import _orjson_default", "from langgraph_sdk._shared.utilities import _orjson_default, is_cross_origin, strip_sensitive_headers")

with open("libs/sdk-py/langgraph_sdk/_async/http.py", "w") as f:
    f.write(content)

with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "r") as f:
    content = f.read()

if "is_cross_origin" not in content:
    content = content.replace("from langgraph_sdk._shared.utilities import _orjson_default", "from langgraph_sdk._shared.utilities import _orjson_default, is_cross_origin, strip_sensitive_headers")

with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "w") as f:
    f.write(content)
