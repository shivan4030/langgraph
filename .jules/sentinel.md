## 2024-05-24 - SQL Injection Risk with f-strings for Database Identifiers
**Vulnerability:** Found f-strings used for dynamic SQL query generation for table identifiers (`f"CREATE TABLE IF NOT EXISTS {table} (v INTEGER PRIMARY KEY)"`) in the postgres storage module.
**Learning:** Using Python string interpolation instead of database driver parameterized queries or composition APIs opens the door to SQL injection, even if the current caller is a hardcoded internal string. This is particularly risky when constructing table names.
**Prevention:** In `psycopg` (v3), enforce the use of `psycopg.sql.SQL` and `psycopg.sql.Identifier` whenever identifiers like table names need to be injected into SQL queries dynamically to guarantee safe sanitization.
