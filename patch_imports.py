import re

with open("libs/sdk-py/langgraph_sdk/_async/http.py", "r") as f:
    async_content = f.read()

import_pattern = r"(from langgraph_sdk\._shared\.utilities import \([\s\S]+?)\)"
import_replacement = r"\1    is_cross_origin,\n    strip_sensitive_headers,\n)"

if "is_cross_origin" not in async_content:
    async_content = re.sub(import_pattern, import_replacement, async_content)

with open("libs/sdk-py/langgraph_sdk/_async/http.py", "w") as f:
    f.write(async_content)


with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "r") as f:
    sync_content = f.read()

if "is_cross_origin" not in sync_content:
    sync_content = re.sub(import_pattern, import_replacement, sync_content)

with open("libs/sdk-py/langgraph_sdk/_sync/http.py", "w") as f:
    f.write(sync_content)
