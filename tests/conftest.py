"""Shared fixtures and synthetic in-memory test databases."""
import sqlite3
import pandas as pd

def create_in_memory_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE dim_plant (
            plant_id INTEGER PRIMARY KEY,
            plant_name TEXT NOT NULL
        );
    """)
    conn.execute("""
        CREATE TABLE dim_machine (
            machine_id INTEGER PRIMARY KEY,
            plant_id INTEGER,
            machine_name TEXT,
            machine_type TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE fact_production (
            production_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_id INTEGER,
            plant_id INTEGER,
            machine_id INTEGER,
            shift_id INTEGER,
            product_id INTEGER,
            units_produced INTEGER,
            units_defective INTEGER,
            operating_hours REAL,
            downtime_hours REAL,
            energy_kwh REAL,
            wear_index REAL
        );
    """)
    conn.execute("INSERT INTO dim_plant VALUES (1, 'Hazira Heavy Engineering');")
    conn.execute("INSERT INTO dim_machine VALUES (1, 1, 'CNC-01', 'CNC Cutting');")
    conn.execute("INSERT INTO fact_production VALUES (1, 1, 1, 1, 1, 1, 120, 2, 7.5, 0.5, 450.0, 32.5);")
    conn.commit()
    return conn
