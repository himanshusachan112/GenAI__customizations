---
name: data-quality-checker
description: Generates data quality assertion checks, null audits, and schema validations for PySpark DataFrames and Delta/Iceberg tables.
---

# Data Quality Assurance Skill

When performing data quality checks or when the user invokes `/data-quality`:

1. **Schema Integrity:**
   - Verify column names match expected `snake_case` patterns.
   - Assert non-nullability on Primary Keys (`assert_no_nulls`).

2. **Distribution & Value Checks:**
   - Check numeric ranges (e.g., `amount >= 0`).
   - Validate timestamp consistency (`event_time <= current_timestamp()`).

3. **Output Format:**
   Generate PySpark data validation code using the standard project wrapper pattern:

```python
from pyspark.sql import DataFrame
import pyspark.sql.functions as F


def validate_dataframe(df: DataFrame, pk_col: str) -> bool:
    """Executes baseline data quality checks on the provided PySpark DataFrame."""
    null_pk_count = df.filter(F.col(pk_col).isNull()).count()
    if null_pk_count > 0:
        raise ValueError(f"Data Quality Alert: Found {null_pk_count} nulls in Primary Key column '{pk_col}'.")
    return True
```
