-- View computing daily machine OEE metrics
CREATE VIEW IF NOT EXISTS v_oee_daily AS
SELECT
    p.date_id,
    p.machine_id,
    m.machine_type,
    pl.plant_name,
    ROUND(SUM(p.operating_hours) / (COUNT(DISTINCT p.shift_id) * 8.0), 4) AS availability,
    ROUND(SUM(p.units_produced) * 1.0 / NULLIF(SUM(p.operating_hours * 12.0), 0), 4) AS performance_rate,
    ROUND(SUM(p.units_produced - p.units_defective) * 1.0 / NULLIF(SUM(p.units_produced), 0), 4) AS quality_rate,
    SUM(p.units_produced) AS total_units,
    SUM(p.units_defective) AS total_defects,
    ROUND(SUM(p.downtime_hours), 2) AS total_downtime
FROM fact_production p
JOIN dim_machine m ON p.machine_id = m.machine_id
JOIN dim_plant pl ON p.plant_id = pl.plant_id
GROUP BY p.date_id, p.machine_id;
