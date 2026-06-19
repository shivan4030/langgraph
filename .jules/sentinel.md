## 2024-05-18 - SQL Injection in Table Creation
**Vulnerability:** SQL Injection via f-strings when interpolating table names in `_get_version` inside `checkpoint-postgres` library base and async versions.
**Learning:** Even internal or utility functions can be exposed to injection if they perform dynamic SQL construction using string interpolation instead of proper SQL identifier escaping like `psycopg.sql.SQL` and `psycopg.sql.Identifier`.
**Prevention:** Always use proper parameterized queries or the specific SQL interpolation libraries provided by the database driver (like `psycopg.sql`) when dynamic identifiers are required.
