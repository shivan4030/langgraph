import ast
with open("libs/checkpoint/langgraph/checkpoint/serde/jsonplus.py") as f:
    code = f.read()
ast.parse(code)
print("Syntax OK")
