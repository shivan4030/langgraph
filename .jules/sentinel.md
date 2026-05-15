
## 2024-05-24 - [Fix Dockerfile ENV Single-Quote Injection]
**Vulnerability:** T5: Dockerfile ENV Single-Quote Injection via config values containing single quotes.
**Learning:** Config values from langgraph.json were serialized via json.dumps() and embedded in single-quoted ENV lines. json.dumps() does not escape single quotes, allowing for injection of Dockerfile commands.
**Prevention:** Always escape single quotes when embedding values into single-quoted strings in Dockerfiles (e.g. `.replace("'", r"'\''")`).
