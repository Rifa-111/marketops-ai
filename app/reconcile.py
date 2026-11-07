from dataclasses import dataclass

@dataclass(frozen=True)
class Break:
    trade_id: str
    category: str
    explanation: str

def reconcile(internal: list[dict], external: list[dict]) -> list[Break]:
    """Compare synthetic trade feeds by trade ID."""
    ext = {str(t["trade_id"]): t for t in external}
    results = []
    for trade in internal:
        tid = str(trade["trade_id"])
        other = ext.get(tid)
        if other is None:
            results.append(Break(tid, "missing_external", "No counterparty record"))
        elif int(trade["quantity"]) != int(other["quantity"]):
            results.append(Break(tid, "quantity_mismatch", "Internal and external quantities differ"))
        elif abs(float(trade["price"]) - float(other["price"])) > 0.0001:
            results.append(Break(tid, "price_mismatch", "Internal and external prices differ"))
    return results
