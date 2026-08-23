"""Operational threshold alert rule engine."""
from typing import List, Dict, Any
from lt_hazira_platform.core.constants import WARNING_FAILURE_RISK, CRITICAL_FAILURE_RISK

def evaluate_machine_alerts(machine_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    alerts = []
    for m in machine_records:
        wear = m.get("wear_index", 0)
        risk = m.get("failure_risk", 0.0)
        
        if risk >= CRITICAL_FAILURE_RISK or wear >= 85:
            alerts.append({
                "machine_id": m.get("machine_id"),
                "severity": "CRITICAL",
                "message": f"Critical risk ({risk:.2f}) or elevated wear index ({wear:.1f})"
            })
        elif risk >= WARNING_FAILURE_RISK or wear >= 70:
            alerts.append({
                "machine_id": m.get("machine_id"),
                "severity": "WARNING",
                "message": f"Elevated failure risk ({risk:.2f}) or wear index ({wear:.1f})"
            })
    return alerts
