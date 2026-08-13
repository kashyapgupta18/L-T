"""Overall Equipment Effectiveness (OEE) calculations."""
from dataclasses import dataclass
from typing import Dict, Any
from lt_hazira_platform.core.constants import SHIFT_HOURS

@dataclass
class OEEResult:
    availability: float
    performance: float
    quality: float
    oee: float

def calculate_oee(operating_hours: float, downtime_hours: float,
                  units_produced: int, ideal_cycle_rate: float,
                  units_defective: int) -> OEEResult:
    planned_hours = SHIFT_HOURS
    availability = max(0.0, min(1.0, operating_hours / planned_hours)) if planned_hours > 0 else 0.0
    
    expected_units = operating_hours * ideal_cycle_rate
    performance = max(0.0, min(1.0, units_produced / expected_units)) if expected_units > 0 else 0.0
    
    good_units = max(0, units_produced - units_defective)
    quality = max(0.0, min(1.0, good_units / units_produced)) if units_produced > 0 else 1.0
    
    oee = round(availability * performance * quality, 4)
    return OEEResult(round(availability, 4), round(performance, 4), round(quality, 4), oee)
