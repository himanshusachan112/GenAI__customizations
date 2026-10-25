---
description: Rewrite SQL with nested subqueries into readable CTEs with explicit partition bounds.
argument-hint: "[SQL file or pasted query]"
---

# /optimize-sql

Rewrite the target SQL for readability, maintainability, and warehouse efficiency.

## Optimization Rules

1. Replace deeply nested subqueries with named CTEs.
2. Preserve query semantics unless a behavioral change is explicitly requested.
3. Use UPPERCASE SQL keywords and `snake_case` identifiers.
4. Add explicit partition predicates for partitioned tables, such as:
   - Date windows.
   - Ingestion date bounds.
   - Business partition filters.
5. Avoid `SELECT *` in production-facing SQL.
6. Use explicit join types and clear join keys.
7. Keep audit columns such as `created_at` and `updated_at` in final mutable-table outputs.

## Output Format

Return:

1. The optimized SQL.
2. A short explanation of each structural change.
3. Any assumptions required for partition columns or date bounds.
