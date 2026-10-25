---
description: Review PySpark and data pipeline code for distributed execution, partition pruning, and skew-safe joins.
argument-hint: "[pipeline path or file glob]"
---

# /review-pipeline

Run a focused architectural review of the selected pipeline code.

## Review Scope

1. Identify unsafe distributed execution patterns:
   - `.collect()` on non-aggregated DataFrames.
   - `.toPandas()` on unbounded DataFrames.
   - Driver-side loops over DataFrame rows.
2. Verify partition pruning:
   - Confirm reads against partitioned sources include explicit partition bounds.
   - Flag scans that do not constrain date, ingestion, or business partition columns.
3. Check join skew handling:
   - Identify joins on low-cardinality or known skewed keys.
   - Recommend broadcast joins, salting, pre-aggregation, or skew hints only when supported by the runtime.
4. Confirm audit and lineage expectations:
   - Validate `created_at` and `updated_at` are added or preserved.
   - Confirm transformation outputs retain useful lineage metadata.

## Output Format

Return findings as a concise table:

| Severity | File | Lines | Finding | Recommended Fix |
| --- | --- | --- | --- | --- |

If no issues are found, state that the reviewed pipeline has no detected `.collect()` abuse, missing partition bounds, or unhandled join-skew risks.
