"""Equipment asset catalog endpoints."""
from fastapi import APIRouter
from lt_hazira_platform.core.db_connection import execute_query
from lt_hazira_platform.api.schemas import MachineInfo
from typing import List

router = APIRouter(prefix="/machines", tags=["Machines"])

@router.get("", response_model=List[MachineInfo])
def list_machines():
    sql = """
        SELECT m.machine_id, m.machine_name, m.machine_type, pl.plant_name
        FROM dim_machine m
        JOIN dim_plant pl ON m.plant_id = pl.plant_id
        ORDER BY m.machine_id
    """
    try:
        rows = execute_query(sql)
        return [MachineInfo(**dict(r)) for r in rows]
    except Exception:
        return []
