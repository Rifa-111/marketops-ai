# MarketOps AI v0.1.0

Initial alpha release of MarketOps AI, a synthetic-data trade reconciliation and exception intelligence platform.

## Included
- FastAPI REST endpoints for reconciliation and exception workflows
- SQLAlchemy persistence with SQLite and PostgreSQL support
- Deterministic investigation suggestions and human-controlled exception state changes
- Audit history, basic Prometheus metrics and health endpoint
- CLI for reconciling two synthetic trade CSV files
- Docker configuration, automated tests and Terraform S3 infrastructure example

## Installation

Install the attached wheel using `pip install marketops_ai-0.1.0-py3-none-any.whl` (use the downloaded file path).

Run `marketops-ai data/internal.csv data/external.csv` from a checkout of the repository to test the CLI.

## Scope and limitations
Alpha software for demonstration and development using synthetic data. No real financial records or client data. The triage engine uses deterministic rules, not an integrated generative AI model. AWS integration, enterprise authentication and production-grade concurrency controls are not implemented. Do not expose the demonstration credentials publicly.
