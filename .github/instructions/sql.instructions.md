---
applyTo: "**/*.sql"
---
# SQL & Data Warehouse Standards

## Syntax & Formatting
- Write all SQL keywords in UPPERCASE, including `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, and `WITH`.
- Use `snake_case` for all table names, column names, aliases, schemas, and database objects.
- Format complex queries using Common Table Expressions (CTEs) rather than deeply nested subqueries.
- Explicitly define join types such as `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, or `FULL OUTER JOIN`; avoid implicit comma joins.

## Performance & Optimization
- Every table scan on partitioned tables must include explicit partition filter predicates, such as `WHERE date >= current_date() - INTERVAL '30' DAY`.
- Select only required columns instead of using `SELECT *` in production queries.
- Prefer set-based operations over row-by-row procedural logic.
- Ensure joins use appropriate keys and avoid accidental cross joins.

## Data Modeling & Auditing
- Include audit columns for mutable warehouse tables where applicable: `created_at`, `updated_at`, `is_current`, and `valid_to`.
- Use timestamp-based auditing for CDC and SCD Type 2 tables.
- Keep migration scripts deterministic, repeatable, and safe to review.
