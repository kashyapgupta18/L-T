-- Sample analytical queries. Written against SQLite; the JOINs and aggregates
-- are standard ANSI SQL and port cleanly to Postgres/MySQL/SQL Server.

-- 1. Which machine had the highest total energy consumption?
SELECT m.machine_id, m.machine_name, p.plant_name,
       ROUND(SUM(f.energy_consumed_kwh), 1) AS total_energy_kwh
FROM fact_production f
JOIN dim_machine m ON f.machine_id = m.machine_id
JOIN dim_plant p ON m.plant_id = p.plant_id
GROUP BY m.machine_id, m.machine_name, p.plant_name
ORDER BY total_energy_kwh DESC
LIMIT 10;

-- 2. Monthly production trend by plant
SELECT p.plant_name, d.year, d.month,
       ROUND(SUM(f.produced_qty), 0) AS total_produced
FROM fact_production f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_plant p ON f.plant_id = p.plant_id
GROUP BY p.plant_name, d.year, d.month
ORDER BY p.plant_name, d.year, d.month;

-- 3. Overall Equipment Effectiveness proxy: availability x quality
-- (Availability = 1 - downtime share of an 8-hour shift; Quality = 1 - defect rate)
SELECT m.machine_id, m.machine_name,
       ROUND(AVG(1 - (f.downtime_minutes / 480.0)), 3) AS avg_availability,
       ROUND(AVG(1 - (CAST(f.defective_qty AS REAL) / NULLIF(f.produced_qty, 0))), 3) AS avg_quality,
       ROUND(AVG(1 - (f.downtime_minutes / 480.0)) * AVG(1 - (CAST(f.defective_qty AS REAL) / NULLIF(f.produced_qty, 0))), 3) AS oee_proxy
FROM fact_production f
JOIN dim_machine m ON f.machine_id = m.machine_id
GROUP BY m.machine_id, m.machine_name
ORDER BY oee_proxy ASC
LIMIT 10;

-- 4. Maintenance cost by type and plant
SELECT p.plant_name, fm.maintenance_type,
       COUNT(*) AS n_events,
       ROUND(SUM(fm.cost_inr), 0) AS total_cost_inr,
       ROUND(AVG(fm.duration_minutes), 0) AS avg_duration_minutes
FROM fact_maintenance fm
JOIN dim_machine m ON fm.machine_id = m.machine_id
JOIN dim_plant p ON m.plant_id = p.plant_id
GROUP BY p.plant_name, fm.maintenance_type
ORDER BY total_cost_inr DESC;

-- 5. Failure rate by machine type
SELECT m.machine_type,
       COUNT(*) AS total_shifts,
       SUM(f.failure_event) AS failure_shifts,
       ROUND(100.0 * SUM(f.failure_event) / COUNT(*), 2) AS failure_rate_pct
FROM fact_production f
JOIN dim_machine m ON f.machine_id = m.machine_id
GROUP BY m.machine_type
ORDER BY failure_rate_pct DESC;

-- 6. Revenue-division-style rollup: production value trend by product category
-- (using produced_qty as a stand-in volume metric since this is a manufacturing,
--  not a revenue, dataset — see README for why no rupee revenue figure is invented)
SELECT pr.category, d.year, d.month,
       ROUND(SUM(f.produced_qty), 0) AS total_units_produced
FROM fact_production f
JOIN dim_product pr ON f.product_id = pr.product_id
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY pr.category, d.year, d.month
ORDER BY pr.category, d.year, d.month;
