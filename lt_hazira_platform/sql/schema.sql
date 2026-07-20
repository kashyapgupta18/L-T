-- L&T Hazira Smart Manufacturing Analytics Platform
-- Star schema: one fact table for production, one for maintenance, five dimensions.
-- Written for SQLite here (so the project runs with zero setup), but the DDL
-- is standard enough to port to PostgreSQL/MySQL/SQL Server with minor type tweaks
-- (e.g. TEXT -> VARCHAR, and add proper DATE types instead of storing date_id as text).

DROP TABLE IF EXISTS fact_production;
DROP TABLE IF EXISTS fact_maintenance;
DROP TABLE IF EXISTS dim_plant;
DROP TABLE IF EXISTS dim_machine;
DROP TABLE IF EXISTS dim_shift;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_plant (
    plant_id        TEXT PRIMARY KEY,
    plant_name      TEXT NOT NULL,
    city            TEXT,
    state           TEXT,
    plant_type      TEXT
);

CREATE TABLE dim_machine (
    machine_id                     TEXT PRIMARY KEY,
    plant_id                       TEXT NOT NULL REFERENCES dim_plant(plant_id),
    machine_name                   TEXT NOT NULL,
    machine_type                   TEXT,
    install_date                   TEXT,
    rated_capacity_units_per_hour  REAL,
    base_energy_kwh_per_hour       REAL
);

CREATE TABLE dim_shift (
    shift_id    TEXT PRIMARY KEY,
    shift_name  TEXT NOT NULL,
    start_time  TEXT,
    end_time    TEXT
);

CREATE TABLE dim_product (
    product_id      TEXT PRIMARY KEY,
    product_name    TEXT NOT NULL,
    category        TEXT,
    uom             TEXT
);

CREATE TABLE dim_date (
    date_id         TEXT PRIMARY KEY,   -- YYYYMMDD
    date            TEXT NOT NULL,
    year            INTEGER,
    quarter         INTEGER,
    month           INTEGER,
    day             INTEGER,
    day_of_week     TEXT,
    is_weekend      INTEGER             -- 0/1
);

CREATE TABLE fact_production (
    record_id           INTEGER PRIMARY KEY,
    date_id             TEXT NOT NULL REFERENCES dim_date(date_id),
    plant_id            TEXT NOT NULL REFERENCES dim_plant(plant_id),
    machine_id          TEXT NOT NULL REFERENCES dim_machine(machine_id),
    shift_id            TEXT NOT NULL REFERENCES dim_shift(shift_id),
    product_id          TEXT NOT NULL REFERENCES dim_product(product_id),
    planned_qty         REAL,
    produced_qty        REAL,
    defective_qty       INTEGER,
    downtime_minutes    REAL,
    energy_consumed_kwh REAL,
    failure_event       INTEGER,        -- 0/1
    machine_wear_index  REAL
);

CREATE TABLE fact_maintenance (
    maintenance_id      TEXT PRIMARY KEY,
    machine_id          TEXT NOT NULL REFERENCES dim_machine(machine_id),
    date_id             TEXT NOT NULL REFERENCES dim_date(date_id),
    maintenance_type    TEXT,           -- 'Preventive' or 'Corrective'
    duration_minutes    REAL,
    cost_inr            REAL,
    technician_team     TEXT
);

CREATE INDEX idx_fact_prod_machine ON fact_production(machine_id);
CREATE INDEX idx_fact_prod_date ON fact_production(date_id);
CREATE INDEX idx_fact_prod_plant ON fact_production(plant_id);
CREATE INDEX idx_fact_maint_machine ON fact_maintenance(machine_id);
