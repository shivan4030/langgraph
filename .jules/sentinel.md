## 2024-06-18 - Prevent SQL Injection with Table Names
**Vulnerability:** The table names for migrations were interpolated into raw strings (`f"SELECT v FROM {table}"`) which could be vulnerable to SQL injection if `table` was ever constructed from user input.
**Learning:** Even internal utility functions like `_get_version` should follow secure coding practices to prevent future misuse. Table name interpolation is a common vector when adding dynamic features.
**Prevention:** Always use `psycopg.sql.SQL` and `psycopg.sql.Identifier` for dynamically interpolating table names or identifiers into SQL queries in psycopg.
