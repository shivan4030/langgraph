## 2025-02-14 - [Insecure Dynamic SQL Query Construction via f-strings]
**Vulnerability:** Found `table` names being directly interpolated into `CREATE TABLE` and `SELECT` SQL queries in `_get_version` function in Postgres checkpointers (`aio.py` and `base.py`). This dynamic interpolation using standard f-strings bypasses normal parameterization.
**Learning:** Developers sometimes use f-strings for object names (tables, columns) because standard parameterization `%s` only works for values. This exposes the database to potential SQL Injection if these identifiers ever become attacker-controlled.
**Prevention:** Always use `psycopg.sql` constructs (e.g., `sql.SQL`, `sql.Identifier`) for dynamic queries that involve variable table names or column names in Postgres.
