"""Pydantic schemas for request validation and response serialization."""
from pydantic import BaseModel, Field
from typing import List, Optional

class PredictionRequest(BaseModel):
    wear_index: float = Field(..., ge=0.0, le=100.0, description="Current wear index 0-100")
    days_since_last_maintenance: float = Field(..., ge=0.0, description="Days elapsed since maintenance")
    prev_shift_downtime: float = Field(0.0, ge=0.0, le=8.0, description="Hours of downtime in previous shift")
    avg_downtime_last_5_shifts: float = Field(0.0, ge=0.0, le=8.0, description="Rolling average downtime")
    machine_age_years: float = Field(5.0, ge=0.0, description="Equipment operational age in years")

class PredictionResponse(BaseModel):
    failure_risk: float
    risk_level: str
    recommendation: str

class MachineInfo(BaseModel):
    machine_id: int
    machine_name: str
    machine_type: str
    plant_name: str

class OEESummaryResponse(BaseModel):
    plant_name: str
    availability: float
    performance: float
    quality: float
    overall_oee: float
