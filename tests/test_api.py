import os
os.environ["DATABASE_URL"] = "sqlite:///./test_marketops.db"
from fastapi.testclient import TestClient
from app.main import app

def test_auth_and_reconciliation():
    with TestClient(app) as client:
        assert client.get("/v1/exceptions").status_code == 401
        data = {"internal": [{"trade_id": "T101", "instrument": "ABC", "quantity": 100, "price": 10}], "external": [{"trade_id": "T101", "instrument": "ABC", "quantity": 90, "price": 10}]}
        headers = {"x-api-key": "local-demo-key"}
        assert client.post("/v1/reconcile", json=data, headers=headers).json()["count"] == 1
        assert client.get("/v1/exceptions/T101:quantity_mismatch/suggestion", headers=headers).status_code == 200
