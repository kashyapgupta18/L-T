-- Query 7: 7-day rolling availability by plant using window functions
SELECT
    date_id,
    plant_name,
    daily_availability,
    ROUND(AVG(daily_availability) OVER (
        PARTITION BY plant_name
        ORDER BY date_id
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 4) AS rolling_7d_availability
FROM (
    SELECT
        p.date_id,
        pl.plant_name,
        ROUND(SUM(p.operating_hours) / (COUNT(DISTINCT p.machine_id) * COUNT(DISTINCT p.shift_id) * 8.0), 4) AS daily_availability
    FROM fact_production p
    JOIN dim_plant pl ON p.plant_id = pl.plant_id
    GROUP BY p.date_id, pl.plant_name
)
ORDER BY plant_name, date_id;
