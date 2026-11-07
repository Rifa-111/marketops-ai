from pydantic import BaseModel, Field

class Suggestion(BaseModel):
    likely_cause: str
    recommended_action: str
    evidence: list[str] = Field(default_factory=list)
    requires_human_approval: bool = True

def suggest(category: str, trade_id: str) -> Suggestion:
    """Deterministic baseline, not a real LLM."""
    actions = {
        "missing_external": ("Counterparty record not received", "Check settlement feed and contact counterparty"),
        "quantity_mismatch": ("Quantity differs between books", "Compare booking amendments and counterparty confirmation"),
        "price_mismatch": ("Price differs between books", "Review execution price and confirmation"),
    }
    cause, action = actions.get(category, ("Unclassified break", "Refer to operations analyst"))
    return Suggestion(likely_cause=cause, recommended_action=action, evidence=[f"trade_id={trade_id}", f"break_type={category}"])
