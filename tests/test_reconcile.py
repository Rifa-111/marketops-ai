from app.reconcile import reconcile
from app.ai import suggest

def test_detects_quantity_break():
    a = [{"trade_id": "T1", "quantity": 100, "price": 5}]
    b = [{"trade_id": "T1", "quantity": 99, "price": 5}]
    assert reconcile(a, b)[0].category == "quantity_mismatch"

def test_idempotent_reconciliation():
    a = [{"trade_id": "T1", "quantity": 100, "price": 5}]
    assert reconcile(a, []) == reconcile(a, [])

def test_ai_never_approves_automatically():
    assert suggest("price_mismatch", "T1").requires_human_approval
