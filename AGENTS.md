# Repository Agent Guidelines

## Agent Operating Principles
1. **Inspect Before Modifying:** Always inspect existing schemas, configurations, source files, and test suites before writing implementation code.
2. **Incremental Validation:** When refactoring or building pipelines, run local unit tests (`pytest`) or dry-run validation scripts to verify correctness.
3. **Traceability:** Ensure data transformations include lineage metadata and audit columns such as `created_at` and `updated_at`.
4. **Scoped Context:** Apply language-specific instructions only to matching files so Python, SQL, and configuration guidance does not conflict.
5. **Minimal Surface Area:** Make focused changes that satisfy the task without rewriting unrelated code or configuration.

## Workspace Boundaries
- Treat repository files as the source of truth; do not rely on assumptions when schemas, DAGs, migrations, or tests can be inspected.
- Preserve existing project structure and naming conventions unless a requested change requires a new structure.
- Do not modify generated artifacts, build outputs, or local environment files unless the task explicitly requires it.

## Task Execution Sequence
1. Inspect the relevant files, schemas, configs, and tests.
2. Identify the smallest coherent change set.
3. Implement the change using repository conventions.
4. Validate with the narrowest relevant test, lint, dry-run, or review command.
5. Summarize the outcome, changed files, and any remaining risk or follow-up.
