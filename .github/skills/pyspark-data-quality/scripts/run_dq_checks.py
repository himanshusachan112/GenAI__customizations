"""Data quality verification helpers for PySpark DataFrames."""

from typing import Any

import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def execute_dq_suite(
    df: DataFrame,
    primary_key: str,
    required_cols: list[str],
) -> dict[str, Any]:
    """Execute core data quality checks for a PySpark DataFrame.

    Args:
        df: Input PySpark DataFrame to validate.
        primary_key: Column name expected to uniquely identify each row.
        required_cols: Column names that must not contain null values.

    Returns:
        A structured dictionary containing the suite status and any failed
        assertions. Each failure includes the check name, column name, and
        invalid row count. The suite validates required column presence,
        primary key non-nullability, primary key uniqueness, and non-null
        constraints for required columns.
    """
    results: dict[str, Any] = {"status": "PASSED", "failures": []}

    expected_columns = set(required_cols + [primary_key])
    missing_columns = sorted(expected_columns.difference(df.columns))
    if missing_columns:
        results["status"] = "FAILED"
        for col_name in missing_columns:
            results["failures"].append(
                {
                    "check": "required_column_exists",
                    "column": col_name,
                    "invalid_row_count": None,
                }
            )
        return results

    null_pk_count = df.filter(F.col(primary_key).isNull()).count()
    if null_pk_count > 0:
        results["status"] = "FAILED"
        results["failures"].append(
            {
                "check": "primary_key_non_null",
                "column": primary_key,
                "invalid_row_count": null_pk_count,
            }
        )

    duplicate_keys = (
        df.filter(F.col(primary_key).isNotNull())
        .groupBy(primary_key)
        .count()
        .filter(F.col("count") > 1)
        .select(primary_key)
    )
    duplicate_count = df.join(duplicate_keys, on=primary_key, how="inner").count()
    if duplicate_count > 0:
        results["status"] = "FAILED"
        results["failures"].append(
            {
                "check": "primary_key_uniqueness",
                "column": primary_key,
                "invalid_row_count": duplicate_count,
            }
        )

    for col_name in required_cols:
        null_count = df.filter(F.col(col_name).isNull()).count()
        if null_count > 0:
            results["status"] = "FAILED"
            results["failures"].append(
                {
                    "check": "non_null_constraint",
                    "column": col_name,
                    "invalid_row_count": null_count,
                }
            )

    return results
