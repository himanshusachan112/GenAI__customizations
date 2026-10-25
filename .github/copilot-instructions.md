# Global Repository Standards

## General Engineering
- Never hardcode credentials, connection strings, API tokens, or private keys; always use environment variables or managed secret stores such as AWS Secrets Manager, GCP Secret Manager, or Azure Key Vault.
- Write clean, self-documenting code with clear variable, function, class, table, and configuration names.
- Prefer small, reviewable changes that preserve existing behavior unless a behavior change is explicitly requested.
- Ensure pull requests include unit, integration, or validation coverage for newly added functionality.
- Surface errors explicitly using repository-standard logging or exception handling; avoid silent failures and broad catch-all handlers.

## Security & Compliance
- Validate and sanitize external inputs before using them in file paths, commands, queries, API calls, or serialized payloads.
- Do not commit generated secrets, credentials, local environment files, or machine-specific configuration.
- Keep dependency changes intentional and minimal, and prefer maintained packages with clear provenance.

## Observability
- Use structured logging for application and pipeline events.
- Include useful context in logs, such as operation name, dataset or resource identifier, record counts, duration, status, and correlation or run identifiers when available.
- Do not log sensitive values such as tokens, passwords, personal data, or full connection strings.

## Scoped Instructions
- Python and PySpark-specific rules live in `.github/instructions/python.instructions.md`.
- SQL and data warehouse-specific rules live in `.github/instructions/sql.instructions.md`.
- Agent workflow and collaboration guidance lives in `AGENTS.md`.
