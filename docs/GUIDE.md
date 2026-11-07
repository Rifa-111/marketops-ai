# Architecture and Engineering Considerations

## System overview
MarketOps AI compares synthetic internal trade records with counterparty feeds, records reconciliation discrepancies and provides evidence-linked investigation suggestions. Human review is required for exception resolution.

## Design considerations
1. **Idempotency:** stable exception identifiers prevent repeated ingestion from creating duplicate breaks.
2. **Late-arriving records:** future pipeline iterations should support event time, reprocessing windows and reconciliation backfills.
3. **Concurrency:** application-level version checking is implemented as a demonstration; database-level atomic compare-and-swap remains to be added.
4. **Human oversight:** investigation suggestions do not automatically change trade or exception records.
5. **Observability:** basic request counters and health endpoints exist; quality metrics and distributed traces are future work.
6. **AI grounding:** a future RAG component should retrieve only authorised records and provide citations to source data.
7. **Schema evolution:** ingestion should detect incompatible upstream schema changes before publishing data.
8. **Persistence:** PostgreSQL supports relational integrity; DynamoDB or graph storage could be evaluated for specific access patterns.
9. **Model governance:** any future LLM should be evaluated on representative cases and tracked using versioned datasets and MLflow.
10. **Operational resilience:** add timeouts, retry policies, migrations, recovery procedures and release controls before deployment.

## Current implementation
- Python/FastAPI API and Pydantic validation
- SQLAlchemy with SQLite locally and PostgreSQL via Docker
- Deterministic reconciliation and triage suggestions
- Audit records and exception state transitions
- GitHub Actions, pytest, Ruff and Docker build
- Terraform configuration for AWS S3

## Planned extensions
- AWS Glue, Lambda, Step Functions and event-driven S3 ingestion
- OpenTelemetry, CloudWatch and alerting dashboards
- RAG retrieval, prompt-injection tests, MLflow experiments and evaluation harness
- OAuth2/OIDC, RBAC, secrets management and least-privilege IAM
- Alembic migrations and concurrency-safe database updates
- DynamoDB event storage, graph-based dependency analysis and Kafka ingestion
- Canary releases and production deployment pipelines

All datasets are synthetic. No claims of operational savings or real-world financial impact are made.
