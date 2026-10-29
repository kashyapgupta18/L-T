# Database Design & Optimization

## Star Schema Optimization
- Foreign keys enabled via PRAGMA foreign_keys = ON.
- WAL (Write-Ahead Logging) journal mode for concurrency during ETL loads.
- Multi-column composite indexes on high-frequency join criteria:
  - `(date_id, machine_id)`
  - `(plant_id, date_id)`
