-- Composite and single-column indices for fast aggregation
CREATE INDEX IF NOT EXISTS idx_prod_date_machine ON fact_production(date_id, machine_id);
CREATE INDEX IF NOT EXISTS idx_prod_plant_date ON fact_production(plant_id, date_id);
CREATE INDEX IF NOT EXISTS idx_prod_machine_shift ON fact_production(machine_id, shift_id);
CREATE INDEX IF NOT EXISTS idx_maint_machine_date ON fact_maintenance(machine_id, date_id);
CREATE INDEX IF NOT EXISTS idx_maint_type ON fact_maintenance(maintenance_type);
