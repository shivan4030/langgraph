## 2024-05-18 - Fix SQL Injection in dynamic table creation for Postgres Store
**Vulnerability:** Found f-strings being used to interpolate table names directly into `CREATE TABLE` and `SELECT` SQL queries in `libs/checkpoint-postgres/langgraph/store/postgres/base.py` and `aio.py`.
**Learning:** This existed because `psycopg` v3's safe dynamic query builder (`psycopg.sql.SQL` and `psycopg.sql.Identifier`) wasn't utilized for constructing DDL queries, leading to the use of Python string interpolation.
**Prevention:** Always use `psycopg.sql` constructs for safe query building involving dynamic identifiers like table or column names, and avoid using `sql` as a local variable name when the `psycopg.sql` module is imported to prevent shadowing errors.
