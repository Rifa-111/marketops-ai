import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Header, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from .models import Base, engine, SessionLocal, Trade, ExceptionRecord, AuditEvent
from .reconcile import reconcile
from .ai import suggest, Suggestion

REQUESTS = Counter("marketops_api_requests_total", "Requests", ["route"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="MarketOps AI", version="0.1.0", lifespan=lifespan)

def db_session():
    with SessionLocal() as db:
        yield db

def actor(x_api_key: str | None = Header(default=None)) -> str:
    expected = os.getenv("API_KEY", "local-demo-key")
    if x_api_key != expected:
        raise HTTPException(401, "Invalid API key")
    return "demo-analyst"

class TradeInput(BaseModel):
    trade_id: str = Field(min_length=1)
    instrument: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

class ReconcileRequest(BaseModel):
    internal: list[TradeInput]
    external: list[TradeInput]

class StatusChange(BaseModel):
    status: str
    expected_version: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/v1/reconcile")
def run_reconciliation(payload: ReconcileRequest, db: Session = Depends(db_session), user: str = Depends(actor)):
    REQUESTS.labels("reconcile").inc()
    breaks = reconcile([x.model_dump() for x in payload.internal], [x.model_dump() for x in payload.external])
    for t in payload.internal:
        if not db.get(Trade, t.trade_id):
            db.add(Trade(id=t.trade_id, instrument=t.instrument, quantity=t.quantity, price=t.price))
    db.flush()
    for b in breaks:
        key = f"{b.trade_id}:{b.category}"
        if not db.get(ExceptionRecord, key):
            db.add(ExceptionRecord(id=key, trade_id=b.trade_id, category=b.category, status="open"))
            db.add(AuditEvent(exception_id=key, actor=user, action="created"))
    db.commit()
    return {"breaks": [b.__dict__ for b in breaks], "count": len(breaks)}

@app.get("/v1/exceptions")
def list_exceptions(status: str | None = None, limit: int = 50, db: Session = Depends(db_session), user: str = Depends(actor)):
    query = select(ExceptionRecord).order_by(ExceptionRecord.id).limit(min(max(limit, 1), 100))
    if status:
        query = query.where(ExceptionRecord.status == status)
    return [{"id": x.id, "trade_id": x.trade_id, "category": x.category, "status": x.status, "version": x.version} for x in db.scalars(query)]

@app.get("/v1/exceptions/{exception_id}/suggestion", response_model=Suggestion)
def get_suggestion(exception_id: str, db: Session = Depends(db_session), user: str = Depends(actor)):
    record = db.get(ExceptionRecord, exception_id)
    if not record:
        raise HTTPException(404, "Exception not found")
    return suggest(record.category, record.trade_id)

@app.patch("/v1/exceptions/{exception_id}")
def update_exception(exception_id: str, change: StatusChange, db: Session = Depends(db_session), user: str = Depends(actor)):
    record = db.get(ExceptionRecord, exception_id)
    if not record:
        raise HTTPException(404, "Exception not found")
    if record.version != change.expected_version:
        raise HTTPException(409, "Version conflict")
    allowed = {"open": {"investigating"}, "investigating": {"resolved", "open"}, "resolved": set()}
    if change.status not in allowed[record.status]:
        raise HTTPException(409, "Invalid state transition")
    record.status = change.status
    record.version += 1
    db.add(AuditEvent(exception_id=exception_id, actor=user, action=f"status:{change.status}"))
    db.commit()
    return {"id": record.id, "status": record.status, "version": record.version}

@app.get("/v1/exceptions/{exception_id}/history")
def history(exception_id: str, db: Session = Depends(db_session), user: str = Depends(actor)):
    return [{"actor": e.actor, "action": e.action, "created_at": e.created_at.isoformat()} for e in db.scalars(select(AuditEvent).where(AuditEvent.exception_id == exception_id).order_by(AuditEvent.id))]
