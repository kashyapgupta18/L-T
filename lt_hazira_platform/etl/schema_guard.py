"""Foreign key and referential integrity validator."""
import sqlite3
from typing import Dict, List
from lt_hazira_platform.core.exceptions import DataValidationError

def verify_foreign_keys(conn: sqlite3.Connection) -> List[Dict]:
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_key_check;")
    violations = cursor.fetchall()
    results = []
    for v in violations:
        results.append({
            "table": v[0],
            "rowid": v[1],
            "parent": v[2],
            "fkid": v[3]
        })
    if results:
        raise DataValidationError(f"Referential integrity violations detected: {len(results)} rows")
    return results
