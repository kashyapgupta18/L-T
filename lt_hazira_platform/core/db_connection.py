"""Thread-safe database connection manager with WAL mode support."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from lt_hazira_platform.core.config import config
from lt_hazira_platform.core.exceptions import DatabaseConnectionError

@contextmanager
def get_db_connection(db_path: Path = None) -> Generator[sqlite3.Connection, None, None]:
    target_path = db_path or config.db_path
    if not target_path.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        conn = sqlite3.connect(str(target_path), timeout=15.0)
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        raise DatabaseConnectionError(f"Failed to connect to SQLite at {target_path}: {e}") from e
    finally:
        conn.close()

def execute_query(query: str, params: tuple = (), db_path: Path = None) -> list:
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
