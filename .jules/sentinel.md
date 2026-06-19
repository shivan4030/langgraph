## 2024-05-18 - [SQL Injection Risk in Postgres Table Setup]
**Vulnerability:** Potential SQL injection via f-string interpolation of table names in `libs/checkpoint-postgres/langgraph/store/postgres/base.py` and `aio.py`.
**Learning:** Even internal or hardcoded table names should use secure query construction to prevent accidental exposure if the method signature changes or is reused.
**Prevention:** Always use `psycopg.sql.SQL` and `psycopg.sql.Identifier` when dynamically building SQL queries that involve identifiers like table or column names.
