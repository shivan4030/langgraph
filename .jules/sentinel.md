## 2024-05-15 - Prevent SQL Injection via string interpolation in Dynamic Identifiers
**Vulnerability:** SQL Injection via string formatting (f-strings) for dynamic table names in Postgres store implementations.
**Learning:** Using Python string formatting (e.g. `f"SELECT * FROM {table}"`) for identifiers circumvents parameter binding and can lead to SQL injection vulnerabilities, especially if the `table` name ever becomes user-supplied.
**Prevention:** Always use `psycopg.sql.SQL` and `psycopg.sql.Identifier` to safely quote dynamic identifiers (tables, columns) in psycopg3.
