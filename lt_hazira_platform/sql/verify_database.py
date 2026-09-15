"""Database health and star schema integrity verification script."""
from lt_hazira_platform.core.db_connection import get_db_connection

def verify_tables():
    expected_tables = [
        "dim_date", "dim_plant", "dim_machine", "dim_product", "dim_shift",
        "fact_production", "fact_maintenance"
    ]
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]
        missing = [t for t in expected_tables if t not in tables]
        if missing:
            print(f"[FAIL] Missing tables: {missing}")
            return False
        
        # Check record counts
        for t in expected_tables:
            cursor.execute(f"SELECT COUNT(*) as cnt FROM {t};")
            cnt = cursor.fetchone()["cnt"]
            print(f"[OK] Table {t}: {cnt} rows")
    return True

if __name__ == "__main__":
    verify_tables()
