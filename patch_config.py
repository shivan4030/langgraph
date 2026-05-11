import re

with open("libs/cli/langgraph_cli/config.py", "r") as f:
    content = f.read()

def replace_fn(match):
    var_name = match.group(1)
    json_var = match.group(2)
    # We can do:
    # "ENV %s='%s'" % ("LANGGRAPH_STORE", json.dumps(store_config).replace("'", r"'\''"))
    return f"\"ENV {var_name}='%s'\" % (json.dumps({json_var}).replace(\"'\", r\"'\\''\"))"

new_content = re.sub(
    r"f\"ENV ([A-Z_]+)='\{json\.dumps\((.*?)\)\}'\"",
    replace_fn,
    content
)

with open("libs/cli/langgraph_cli/config.py", "w") as f:
    f.write(new_content)
