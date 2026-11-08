# MarketOps AI — Trade Exception Intelligence Platform

MarketOps AI is a prototype post-trade reconciliation and exception-management platform designed to identify discrepancies between internal trade records and counterparty feeds, maintain auditable exception workflows and support evidence-based investigation.

The platform uses **synthetic financial data** and demonstrates an extensible architecture for data processing, API development, operational controls and AI-assisted exception triage.

## Capabilities
- **Trade reconciliation:** detects missing counterparty records, quantity differences and price discrepancies
- **Exception management:** persistent exception records, workflow status transitions and change history
- **Investigation assistance:** deterministic, evidence-linked root-cause suggestions with mandatory human review
- **Data processing:** CSV ingestion and validation-oriented reconciliation pipeline
- **Service observability:** health checks and Prometheus-compatible metrics
- **Deployment foundations:** Docker, PostgreSQL, automated CI and Terraform-based AWS S3 configuration

## Technology stack

| Layer | Technologies |
|---|---|
| Backend | Python, FastAPI, Pydantic, REST, OpenAPI |
| Data | PostgreSQL, SQLite, SQLAlchemy, CSV |
| Infrastructure | Docker, Docker Compose, Terraform, AWS S3 |
| Quality | pytest, Ruff, GitHub Actions |
| Observability | Prometheus metrics |
| AI extension | Rule-based baseline; LLM/RAG and MLflow integration planned |

## Architecture

```text
Synthetic trade feeds (CSV / API)
             |
       Validation & matching
             |
      Reconciliation engine
             |
    FastAPI + SQLAlchemy
             |
     PostgreSQL / SQLite
             |
   Exceptions + audit trail
             |
 Evidence-based triage suggestions
             |
     Human analyst review
```

## Getting started

**Local Python environment**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

On Windows, activate with `.venv\Scripts\activate`. API documentation is available at http://localhost:8000/docs.

**Docker with PostgreSQL**

```bash
docker compose up --build
```

The example API key is `local-demo-key` and should be supplied in the `x-api-key` header for protected routes.

## Example API request

```bash
curl -X POST http://localhost:8000/v1/reconcile \
  -H 'x-api-key: local-demo-key' \
  -H 'content-type: application/json' \
  -d '{"internal":[{"trade_id":"T1","instrument":"AAPL","quantity":100,"price":210}],"external":[{"trade_id":"T1","instrument":"AAPL","quantity":90,"price":210}]}'
```

Other endpoints include `GET /v1/exceptions`, `GET /v1/exceptions/{exception_id}/suggestion`, `PATCH /v1/exceptions/{exception_id}`, `GET /health` and `GET /metrics`.

## Testing

```bash
pytest -q
ruff check app tests etl
python -m etl.load_csv
```

## Engineering roadmap

- **Data engineering:** AWS Glue jobs, Lambda event handlers, late-arriving data and backfill handling
- **Applied AI:** retrieval-augmented investigation, structured LLM outputs, evaluation datasets and MLflow tracking
- **Security:** OIDC authentication, role-based authorisation and managed secrets
- **Observability:** distributed tracing, CloudWatch alarms and operational dashboards
- **Scalability:** migrations, concurrency-safe updates, event-driven ingestion and workload testing
- **Deployment:** infrastructure automation, controlled releases and rollback strategies

