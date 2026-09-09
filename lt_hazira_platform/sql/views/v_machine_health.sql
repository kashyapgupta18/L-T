-- View representing current equipment health status
CREATE VIEW IF NOT EXISTS v_machine_health AS
SELECT
    m.machine_id,
    m.machine_name,
    m.machine_type,
    pl.plant_name,
    p.wear_index AS latest_wear_index,
    p.operating_hours AS last_shift_operating_hours,
    p.downtime_hours AS last_shift_downtime,
    CASE
        WHEN p.wear_index >= 80 THEN 'CRITICAL'
        WHEN p.wear_index >= 65 THEN 'WARNING'
        ELSE 'NORMAL'
    END AS wear_status
FROM dim_machine m
JOIN dim_plant pl ON m.plant_id = pl.plant_id
JOIN fact_production p ON m.machine_id = p.machine_id
WHERE p.date_id = (SELECT MAX(date_id) FROM fact_production)
  AND p.shift_id = (SELECT MAX(shift_id) FROM fact_production WHERE date_id = p.date_id);
