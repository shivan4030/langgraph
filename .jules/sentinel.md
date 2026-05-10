## 2025-02-28 - Dockerfile ENV Single-Quote Injection
**Vulnerability:** The CLI Dockerfile generation embedded `langgraph.json` values directly into single-quoted `ENV` directives via `json.dumps()`. Because `json.dumps()` does not escape single quotes, a config value containing a single quote could break out of the `ENV` directive, enabling Dockerfile ENV injection.
**Learning:** This existed because standard JSON serialization was assumed safe for embedding inside single quotes, overlooking that JSON strings can contain unescaped single quotes which are interpreted directly by Bash/Dockerfile parsers.
**Prevention:** Always escape single quotes (e.g., replacing `'` with `'\''`) when interpolating data into single-quoted strings in shell or Dockerfile environments.
