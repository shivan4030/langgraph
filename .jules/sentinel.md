## 2025-04-13 - Prevent SQL Injection via string formatting in psycopg
**Vulnerability:** Using Python f-strings to interpolate table names (e.g. `f"CREATE TABLE IF NOT EXISTS {table}...` or `f"SELECT v FROM {table}...`) into SQL queries, exposing the system to potential SQL injection.
**Learning:** When migrating or dynamically creating objects using psycopg, the `psycopg.sql` module provides safe classes (`sql.SQL` and `sql.Identifier`) to compose queries safely, which is preferable to native python string formatting.
**Prevention:** Always use `sql.SQL().format(sql.Identifier(name))` rather than f-strings when dynamic table names or identifiers are required by `psycopg`.
