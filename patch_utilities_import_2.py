with open("libs/sdk-py/langgraph_sdk/_shared/utilities.py", "r") as f:
    content = f.read()

content = content.replace("import urllib.parse\n", "")

if "import urllib.parse" not in content:
    content = content.replace("import os", "import os\nimport urllib.parse")

with open("libs/sdk-py/langgraph_sdk/_shared/utilities.py", "w") as f:
    f.write(content)
