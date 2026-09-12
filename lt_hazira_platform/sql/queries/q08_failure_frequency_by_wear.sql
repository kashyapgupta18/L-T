-- Query 8: Failure frequency correlated with wear index buckets
SELECT
    CASE
        WHEN p.wear_index < 30 THEN '01: 0-29 Low'
        WHEN p.wear_index < 60 THEN '02: 30-59 Medium'
        WHEN p.wear_index < 80 THEN '03: 60-79 High'
        ELSE '04: 80-100 Critical'
    END AS wear_bracket,
    COUNT(p.production_id) AS total_shifts,
    ROUND(AVG(p.downtime_hours), 2) AS avg_downtime_hours,
    ROUND(AVG(p.units_defective * 1.0 / NULLIF(p.units_produced, 0)) * 100, 2) AS defect_rate_pct
FROM fact_production p
GROUP BY wear_bracket
ORDER BY wear_bracket;
