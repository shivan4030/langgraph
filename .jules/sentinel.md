## 2024-05-24 - SQL Injection Vulnerability in Postgres Store migrations

**Vulnerability:** In `libs/checkpoint-postgres`, table names in the `_get_version` setup method were being unsafely interpolated into raw SQL query strings using Python f-strings. This pattern is vulnerable to SQL injection if table names are controlled by user input or modified later without understanding the risk.

**Learning:** This existed because the `table` string arguments (`"store_migrations"` and `"vector_migrations"`) were currently hardcoded at the call site, masking the vulnerability from being actively exploitable. However, string formatting for any SQL identifier breaks the separation of query structure and data and is an unsafe practice.

**Prevention:** Always use the `psycopg.sql` module (`psql.SQL` and `psql.Identifier`) to dynamically build SQL queries involving table names, column names, or other identifiers safely in `checkpoint-postgres`.
