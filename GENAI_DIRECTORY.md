# GenAI Directory Documentation

## Purpose

This document explains the `GenAI` directory structure and how each file contributes to the enterprise AI-assisted data-engineering toolkit.

The directory is organized as a reusable repository-level bundle for data teams working with PySpark, SQL, Airflow, data quality checks, and governed enterprise metadata.

## Directory Map

```text
GenAI
├── AGENTS.md
├── README.md
├── package.json
├── bin
│   └── data-eng-toolkit-setup.js
├── PLUGIN_ARCHITECTURE_DESIGN.md
├── GENAI_DIRECTORY.md
├── setup-toolkit.sh
└── .github
    ├── plugin-manifest.yml
    ├── copilot-instructions.md
    ├── agents
    │   ├── data-engineer.agent.md
    │   └── qa-engineer.agent.md
    ├── commands
    │   ├── optimize-sql.md
    │   └── review-pipeline.md
    ├── hooks
    │   ├── post-gen-validator.py
    │   └── pre-commit-guard.js
    ├── instructions
    │   ├── python.instructions.md
    │   └── sql.instructions.md
    ├── mcp-servers
    │   ├── README.md
    │   ├── enterprise-bigquery.json
    │   └── internal-catalog.json
    └── skills
        ├── data-quality-checker
        │   └── SKILL.md
        └── pyspark-data-quality
            ├── SKILL.md
            ├── resources
            │   └── dq_rules_template.json
            └── scripts
                └── run_dq_checks.py
```

## Root-Level Files

| File | Purpose |
| --- | --- |
| `README.md` | Main repository explanation for scoped instructions, agents, skills, commands, hooks, and MCP templates. |
| `package.json` | Optional internal npm, CLI, or VSIX packaging manifest with validation scripts and setup command mapping. |
| `bin/data-eng-toolkit-setup.js` | Node-based npm binary wrapper that locates a POSIX shell and delegates to `setup-toolkit.sh`. |
| `AGENTS.md` | Agent operating rules for inspection, minimal changes, validation, traceability, and workspace boundaries. |
| `PLUGIN_ARCHITECTURE_DESIGN.md` | Enterprise plugin bundle architecture, distribution model, conceptual manifest, and adoption checklist. |
| `GENAI_DIRECTORY.md` | Directory-level documentation for the toolkit structure and ownership model. |
| `setup-toolkit.sh` | Initialization script for installing the toolkit into target repositories by copy or symlink. |

## `.github` Directory

The `.github` directory contains the reusable AI toolkit assets. These files define how AI assistants should behave, which specialized agents are available, which reusable skills can be loaded, and which deterministic guardrails protect generated artifacts.

### Global Instructions

| File | Purpose |
| --- | --- |
| `.github/plugin-manifest.yml` | Conceptual plugin bundle manifest for registry, scaffold CLI, IDE extension, or future Copilot plugin packaging. |
| `.github/copilot-instructions.md` | Repository-wide standards for secure coding, audit columns, structured logging, validation, and scoped instruction routing. |

### Scoped Instructions

| File | Applies To | Purpose |
| --- | --- | --- |
| `.github/instructions/python.instructions.md` | `**/*.py` | PySpark, Python typing, docstring, logging, data quality, and Airflow orchestration rules. |
| `.github/instructions/sql.instructions.md` | `**/*.sql` | SQL casing, CTEs, partition filters, explicit joins, audit fields, and data warehouse performance rules. |

### Specialized Agents

| File | Role |
| --- | --- |
| `.github/agents/data-engineer.agent.md` | Implements production PySpark ETL, Medallion Lakehouse pipelines, DataFrame optimizations, and Airflow orchestration patterns. |
| `.github/agents/qa-engineer.agent.md` | Validates PySpark transformations, null handling, primary key uniqueness, schema integrity, and `chispa` test coverage. |

### Skills

| Path | Purpose |
| --- | --- |
| `.github/skills/data-quality-checker/SKILL.md` | General data quality assertion, null audit, schema validation, and cleansing guidance. |
| `.github/skills/pyspark-data-quality/SKILL.md` | PySpark-specific data quality workflow for validation, rule selection, and reporting. |
| `.github/skills/pyspark-data-quality/resources/dq_rules_template.json` | Baseline rule template for required columns, uniqueness, timestamp checks, and metric ranges. |
| `.github/skills/pyspark-data-quality/scripts/run_dq_checks.py` | Reusable PySpark validation utility for vectorized data quality checks. |

### Shortcut Commands

| File | Command | Purpose |
| --- | --- | --- |
| `.github/commands/review-pipeline.md` | `/review-pipeline` | Reviews pipeline code for `.collect()` abuse, missing partition pruning, join skew risk, and audit-column preservation. |
| `.github/commands/optimize-sql.md` | `/optimize-sql` | Rewrites nested SQL into CTEs with explicit partition bounds, uppercase keywords, and explicit joins. |

### Deterministic Hooks

| File | Runtime | Purpose |
| --- | --- | --- |
| `.github/hooks/pre-commit-guard.js` | Node.js | Scans generated or staged files for AWS/GCP keys, private key markers, credential-bearing connection strings, generic tokens, and high-risk PII. |
| `.github/hooks/post-gen-validator.py` | Python | Validates generated Airflow DAG files with artifact-free Python syntax checks and `airflow dags test`. |

### MCP Server Templates

| File | Purpose |
| --- | --- |
| `.github/mcp-servers/enterprise-bigquery.json` | Secure metadata-only MCP template for BigQuery schema inspection, partition metadata, and query cost estimates. |
| `.github/mcp-servers/internal-catalog.json` | Secure metadata-only MCP template for DataHub, OpenMetadata, or internal catalog lineage lookup. |
| `.github/mcp-servers/README.md` | Local configuration guide for MCP server templates and required environment variables. |

## Recommended Team Workflow

1. Start from `README.md` to understand the repository behavior.
2. Read `PLUGIN_ARCHITECTURE_DESIGN.md` when adopting or distributing the toolkit across teams.
3. Use `GENAI_DIRECTORY.md` to locate the correct instruction, agent, skill, command, hook, or MCP file.
4. Consume the bundle through a Git submodule, scaffold CLI, internal IDE extension, or future plugin package.
5. Run `setup-toolkit.sh --target <repo> --mode copy` or `setup-toolkit.sh --target <repo> --mode symlink`.
6. Configure environment variables for MCP templates outside the repository.
7. Register hooks in local developer workflows or CI.
8. Use shortcut commands for recurring pipeline and SQL review tasks.
9. Keep repository-specific implementation code separate from this reusable toolkit layer.

## Packaging and Distribution Files

| File | Purpose |
| --- | --- |
| `.github/plugin-manifest.yml` | Declares bundle metadata, supported distribution modes, instruction files, agents, skills, commands, hooks, MCP servers, and setup actions. |
| `package.json` | Declares the private package name `@enterprise/data-eng-copilot-bundle`, exposed setup binary, package files, and validation scripts. |
| `bin/data-eng-toolkit-setup.js` | Provides the cross-platform npm entry point for `data-eng-toolkit-setup`. |
| `setup-toolkit.sh` | Installs toolkit-managed assets into a target Git repository, creates `.vscode/mcp.json`, and installs `.git/hooks/pre-commit`. |

### Setup Script Examples

```sh
tools/data-eng-copilot-bundle/setup-toolkit.sh --target . --mode copy
tools/data-eng-copilot-bundle/setup-toolkit.sh --target . --mode symlink
tools/data-eng-copilot-bundle/setup-toolkit.sh --target . --mode copy --force
```

Use `copy` when the target repository should own a snapshot of the toolkit files. Use `symlink` when the repository consumes the toolkit as a submodule and should automatically reflect submodule updates.

### Package Validation

```sh
npm run validate
```

This validates `package.json`, the Node hook, and the Python DAG validator hook. The package is marked `private` so it cannot be accidentally published to a public registry.

## Ownership

| Area | Recommended Owner |
| --- | --- |
| Global instructions | Enterprise platform or enablement team |
| Scoped Python and SQL standards | Data platform engineering team |
| Agents and skills | AI enablement team with data engineering reviewers |
| Hooks | Security engineering and data platform team |
| MCP templates | Platform engineering and data governance team |
| Plugin manifest and setup script | Enterprise platform or developer-experience team |
| Repository-specific extensions | Application or domain data teams |

## Extension Guidelines

When adding new toolkit capabilities:

1. Keep each capability modular.
2. Avoid embedding environment-specific credentials or endpoints unless they are non-sensitive placeholders.
3. Prefer environment variables for runtime wiring.
4. Document every new agent, skill, command, hook, or MCP server in `README.md` and this directory guide.
5. Add validation commands or smoke-test instructions when executable scripts are introduced.
6. Preserve existing naming conventions and directory layout.

## Quick Validation Commands

```powershell
node --check .github\hooks\pre-commit-guard.js
python .github\hooks\post-gen-validator.py --help
node .github\hooks\pre-commit-guard.js .github\commands\review-pipeline.md
python .github\hooks\post-gen-validator.py --help
```

These checks validate hook syntax and basic command-line behavior without requiring a full Airflow installation.
