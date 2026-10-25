# MCP Server Templates

This directory contains secure Model Context Protocol server definitions for enterprise data platform metadata access.

## enterprise-bigquery

`enterprise-bigquery.json` defines a metadata-only BigQuery MCP template for:

- Listing datasets.
- Describing table schemas.
- Inspecting partitioning and clustering metadata.
- Estimating query cost before execution.

The template intentionally uses environment variables and managed identity or application default credentials. Do not place service account JSON, private keys, or connection strings in this repository.

## internal-catalog

`internal-catalog.json` defines a metadata-only catalog MCP template for systems such as DataHub or OpenMetadata. It supports:

- Dataset ownership lookup.
- Upstream lineage lookup.
- Downstream lineage lookup.
- Table contract retrieval.

Authentication must be supplied by environment variables or managed identity. Raw catalog tokens must not be committed.

## Required Local Wiring

Set the command variables to the approved internal MCP bridge binaries for your environment:

- `ENTERPRISE_BIGQUERY_MCP_COMMAND`
- `INTERNAL_CATALOG_MCP_COMMAND`

Then configure the runtime-specific MCP client to load these JSON definitions.
