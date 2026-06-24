with open("libs/sdk-py/langgraph_sdk/_async/http.py", "r") as f:
    content = f.read()

content = content.replace(
    "from langgraph_sdk._shared.utilities import _orjson_default",
    "from langgraph_sdk._shared.utilities import _orjson_default, is_cross_origin, strip_sensitive_headers"
)

with open("libs/sdk-py/langgraph_sdk/_async/http.py", "w") as f:
    f.write(content)

with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "r") as f:
    content = f.read()

content = content.replace(
    "from langgraph_sdk._shared.utilities import _orjson_default",
    "from langgraph_sdk._shared.utilities import _orjson_default, is_cross_origin, strip_sensitive_headers"
)

with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "w") as f:
    f.write(content)

with open("libs/sdk-py/langgraph_sdk/_shared/utilities.py", "r") as f:
    content = f.read()

content = content.replace("import urllib.parse\n\ndef is_cross_origin", "def is_cross_origin")
if "import urllib.parse" not in content:
    content = content.replace("import os", "import os\nimport urllib.parse")

with open("libs/sdk-py/langgraph_sdk/_shared/utilities.py", "w") as f:
    f.write(content)
