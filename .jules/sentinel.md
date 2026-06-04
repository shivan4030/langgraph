## YYYY-MM-DD - Dockerfile ENV Injection via json.dumps()
**Vulnerability:** Command/Environment injection in CLI-generated Dockerfiles when `json.dumps()` output was interpolated into single-quoted `ENV` declarations. Since `json.dumps()` doesn't escape single quotes, a user-controlled config value containing `'` could break out of the quote and inject malicious variables or Dockerfile instructions.
**Learning:** Standard JSON serializers do not consider shell or Dockerfile string constraints.
**Prevention:** Always escape single quotes explicitly (`.replace("'", r"'\''")`) when inserting serialized strings into single-quoted script or Dockerfile contexts.
