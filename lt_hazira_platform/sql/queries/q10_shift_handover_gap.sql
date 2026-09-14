-- Query 10: Comparison of output variance across shift handovers
SELECT
    s.shift_name,
    COUNT(p.production_id) AS recorded_shifts,
    ROUND(AVG(p.units_produced), 1) AS mean_units_per_shift,
    ROUND(AVG(p.downtime_hours), 2) AS mean_downtime_per_shift,
    ROUND(AVG(p.energy_kwh), 1) AS mean_energy_kwh
FROM fact_production p
JOIN dim_shift s ON p.shift_id = s.shift_id
GROUP BY s.shift_name
ORDER BY mean_units_per_shift DESC;
