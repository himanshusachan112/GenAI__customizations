---
name: pyspark-data-quality
description: Automatically triggers when a user requests data quality validation, null checking, schema assertions, or data cleansing for PySpark DataFrames.
---

# PySpark Data Quality Assurance Skill

When validating data quality or running assertions on PySpark DataFrames:

1. **Rule Selection:**
   - Inspect the input DataFrame schema.
   - Refer to `resources/dq_rules_template.json` for baseline assertion standards, including null bounds, key uniqueness, and range validations.

2. **Script Execution / Code Generation:**
   - Integrate the validation utility located in `scripts/run_dq_checks.py`.
   - Ensure checks are executed using native PySpark vectorization to prevent full-table collects.

3. **Reporting:**
   - Format failed assertions as a structured summary showing the failing check, column name, and invalid row count.
