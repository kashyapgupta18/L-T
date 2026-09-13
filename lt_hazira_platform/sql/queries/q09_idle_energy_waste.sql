-- Query 9: High energy consumption during high downtime shifts
SELECT
    m.machine_name,
    m.machine_type,
    pl.plant_name,
    ROUND(AVG(p.energy_kwh), 2) AS avg_energy_kwh_during_downtime,
    COUNT(p.production_id) AS down_shifts_count
FROM fact_production p
JOIN dim_machine m ON p.machine_id = m.machine_id
JOIN dim_plant pl ON p.plant_id = pl.plant_id
WHERE p.downtime_hours > 3.0
GROUP BY m.machine_name, m.machine_type, pl.plant_name
ORDER BY avg_energy_kwh_during_downtime DESC
LIMIT 10;
