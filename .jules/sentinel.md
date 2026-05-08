## 2025-05-08 - Fix SQL Injection in Table Interpolation
**Vulnerability:** SQL injection risk due to table name strings being interpolated into dynamic SQL queries via f-strings (e.g., `CREATE TABLE IF NOT EXISTS {table}`).
**Learning:** `psycopg` requires using `psycopg.sql.SQL` and `psycopg.sql.Identifier` for safe, parameterised substitution of structural parts of a SQL query (like table names), as typical bind parameters (`%s`) only support query values.
**Prevention:** Avoid f-strings for building SQL queries with dynamic table/schema/column identifiers; instead, compose them utilizing `psycopg.sql`. Also, when importing `from psycopg import sql`, rename iteration variables (like `sql`) to avoid shadowing the module.
