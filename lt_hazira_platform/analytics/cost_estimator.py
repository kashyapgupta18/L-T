"""Financial impact calculation: maintenance expense vs lost production value."""
from dataclasses import dataclass

@dataclass
class FinancialImpactSummary:
    labor_cost: float
    parts_cost: float
    lost_production_value: float
    total_cost: float

def estimate_downtime_loss(downtime_hours: float, labor_cost: float, parts_cost: float,
                           hourly_production_value: float = 12500.0) -> FinancialImpactSummary:
    lost_val = round(downtime_hours * hourly_production_value, 2)
    tot = round(labor_cost + parts_cost + lost_val, 2)
    return FinancialImpactSummary(labor_cost, parts_cost, lost_val, tot)
