-- View summarizing maintenance expenditure by machine and type
CREATE VIEW IF NOT EXISTS v_maintenance_cost AS
SELECT
    pl.plant_name,
    m.machine_type,
    fm.maintenance_type,
    COUNT(fm.maintenance_id) AS event_count,
    ROUND(SUM(fm.duration_hours), 2) AS total_repair_hours,
    ROUND(SUM(fm.cost_labor), 2) AS total_labor_cost,
    ROUND(SUM(fm.cost_parts), 2) AS total_parts_cost,
    ROUND(SUM(fm.cost_labor + fm.cost_parts), 2) AS total_maintenance_expenditure
FROM fact_maintenance fm
JOIN dim_machine m ON fm.machine_id = m.machine_id
JOIN dim_plant pl ON m.plant_id = pl.plant_id
GROUP BY pl.plant_name, m.machine_type, fm.maintenance_type;
