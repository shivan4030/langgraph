## 2025-02-14 - Dockerfile ENV Single-Quote Injection
**Vulnerability:** Shell command injection via unescaped single quotes in `langgraph.json` configuration values during Dockerfile generation.
**Learning:** `json.dumps()` does not escape single quotes. When embedded in single-quoted `ENV` directives (e.g., `ENV VAR='{json}'`), it allows premature string termination and potentially arbitrary code execution during the Docker build process or when running the container.
**Prevention:** Always pass serialized JSON through a sanitizer (e.g., `.replace("'", r"'\''")`) before embedding it into shell-evaluated contexts like Dockerfile `ENV` directives.
