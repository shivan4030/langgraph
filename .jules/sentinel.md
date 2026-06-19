## 2024-05-18 - [PostgresStore Unvalidated Filter Keys]
**Vulnerability:** Unvalidated filter keys passed to Postgres `->` JSON operator.
**Learning:** Even though Postgres parameterization (`value->%s = %s`) protects against traditional SQL injection, failing to validate the key schema still allows malicious actors to send unbounded or malformed payloads, violating the principle of least privilege and inconsistent with `SqliteStore` defenses.
**Prevention:** Ensure uniform validation (`_validate_filter_key`) across all database store implementations.

## 2024-05-18 - [False Positive on Public API Keys]
**Vulnerability:** None. The `SUPABASE_PUBLIC_API_KEY` was flagged as a hardcoded secret.
**Learning:** Client-side telemetry keys (like Supabase anon keys) are meant to be public. Removing them based on generic secret scanning heuristics breaks functionality.
**Prevention:** Contextually verify the purpose of hardcoded credentials before removing them (e.g., checking if it explicitly says "PUBLIC").
