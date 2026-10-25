---
applyTo: "**/*.py"
---
# Python & PySpark Code Standards

## PySpark & Data Quality
- Use the PySpark DataFrame API over raw Spark SQL strings where possible.
- Use explicit schema definitions (`StructType`) for all DataFrame reads instead of inferring schemas from JSON or CSV inputs.
- Avoid `.collect()` and `.toPandas()` on non-aggregated DataFrames; use `.take(n)`, bounded aggregations, or write to storage for inspection.
- Use `chispa` for robust PySpark unit testing assertions.
- Always implement CDC and SCD Type 2 tracking with timestamp-based auditing columns: `created_at`, `updated_at`, `is_current`, and `valid_to`.
- Include lineage metadata and audit fields for transformations where records move between pipeline layers.

## Type Safety & Documentation
- Use strict type hints from the `typing` module or built-in generic types for all function signatures.
- Provide Google-style docstrings for all classes, public functions, pipeline transformations, and utility functions.
- Document arguments, return types, raised exceptions, and important side effects in docstrings.

## Logging & Runtime Behavior
- Log pipeline execution metrics using structured JSON logging.
- Include run identifiers, dataset names, row counts, durations, and status where available.
- Do not use raw `print()` statements for pipeline or application logging.

## Airflow & Orchestration
- Ensure Airflow DAGs define explicit task dependencies with `>>`.
- Configure DAG tasks with `retries=3` and exponential backoff unless a task-specific reason requires otherwise.
