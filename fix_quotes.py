import json

def generate_docker_env(var_name, var_value):
    escaped_val = json.dumps(var_value).replace("'", "'\\''")
    return f"ENV {var_name}='{escaped_val}'"

print(generate_docker_env("MY_VAR", {"key": "value'"}))
