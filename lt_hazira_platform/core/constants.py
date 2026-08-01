"""Manufacturing domain constants for L&T Hazira Platform."""

PLANTS = [
    "Hazira Heavy Engineering",
    "Hazira Process Equipment",
    "Hazira Modular Fabrication",
    "Powai Precision Unit",
    "Coimbatore Components Unit",
]

MACHINE_TYPES = [
    "CNC Cutting",
    "Heavy Press Forming",
    "Welding Robot",
    "Shot Blasting",
    "Sub-Arc Welding",
    "Rolling Mill",
    "CNC Machining Center",
    "Heat Treatment Furnace",
]

SHIFTS = ["Morning", "Evening", "Night"]
SHIFT_HOURS = 8.0
TOTAL_MACHINES = 40
SIMULATION_DAYS = 210

# Operational thresholds
DEFAULT_OEE_TARGET = 0.85
CRITICAL_FAILURE_RISK = 0.60
WARNING_FAILURE_RISK = 0.35
MAX_ALLOWABLE_DOWNTIME_HOURS = 8.0
