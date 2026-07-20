# Power BI Dashboard — Setup Guide

A quick note on scope: a `.pbix` file can only be created inside Power BI
Desktop itself, there's no way to script one from outside the app. So instead
of a fake or empty file claiming to be a dashboard, this gives you everything
needed to build the real one in about 15 minutes: the data model (already
normalized, already exported as CSV/SQLite), and the exact DAX measures to
drop in.

## 1. Get the data in

Open Power BI Desktop → **Get Data** → **SQLite database** → point it at
`data/hazira_manufacturing.db`. If the SQLite connector isn't installed,
use **Get Data → Text/CSV** instead and import each file from `data/*.csv`.

Load these seven tables: `dim_plant`, `dim_machine`, `dim_shift`,
`dim_product`, `dim_date`, `fact_production`, `fact_maintenance`.

## 2. Build the relationships (Model view)

Power BI should auto-detect most of these from matching column names, but
check each one:

- `fact_production[plant_id]` → `dim_plant[plant_id]`
- `fact_production[machine_id]` → `dim_machine[machine_id]`
- `fact_production[shift_id]` → `dim_shift[shift_id]`
- `fact_production[product_id]` → `dim_product[product_id]`
- `fact_production[date_id]` → `dim_date[date_id]`
- `fact_maintenance[machine_id]` → `dim_machine[machine_id]`
- `fact_maintenance[date_id]` → `dim_date[date_id]`
- `dim_machine[plant_id]` → `dim_plant[plant_id]`

Mark `dim_date` as a **Date Table** (Modeling tab → Mark as Date Table) so
time-intelligence functions like `SAMEPERIODLASTYEAR` work correctly if you
add them later.

## 3. Core DAX measures

```dax
Total Units Produced = SUM(fact_production[produced_qty])

Total Defective Units = SUM(fact_production[defective_qty])

Defect Rate % =
DIVIDE([Total Defective Units], [Total Units Produced], 0) * 100

Total Downtime (hrs) =
SUM(fact_production[downtime_minutes]) / 60

Avg Downtime per Shift (min) =
AVERAGE(fact_production[downtime_minutes])

Total Energy (kWh) = SUM(fact_production[energy_consumed_kwh])

Energy per Unit (kWh) =
DIVIDE([Total Energy (kWh)], [Total Units Produced], 0)

Failure Count = SUM(fact_production[failure_event])

Failure Rate % =
DIVIDE([Failure Count], COUNTROWS(fact_production), 0) * 100

Availability % =
(1 - DIVIDE(SUM(fact_production[downtime_minutes]), COUNTROWS(fact_production) * 480, 0)) * 100

Quality % = 100 - [Defect Rate %]

OEE Proxy % =
[Availability %] * [Quality %] / 100

Total Maintenance Cost = SUM(fact_maintenance[cost_inr])

Preventive Maintenance Cost =
CALCULATE([Total Maintenance Cost], fact_maintenance[maintenance_type] = "Preventive")

Corrective Maintenance Cost =
CALCULATE([Total Maintenance Cost], fact_maintenance[maintenance_type] = "Corrective")

Preventive Cost Share % =
DIVIDE([Preventive Maintenance Cost], [Total Maintenance Cost], 0) * 100
```

## 4. Suggested pages

**Page 1 — Executive Overview**
KPI cards: Total Units Produced, Failure Rate %, Availability %, OEE Proxy %,
Total Maintenance Cost. Line chart of weekly production. Bar chart of
production by plant.

**Page 2 — Production & Quality**
Matrix of plant × product category with Total Units Produced and Defect Rate %.
Trend line of Defect Rate % over time, filterable by machine type.

**Page 3 — Downtime & Energy**
Bar chart: top 10 machines by Total Energy (kWh). Bar chart: Avg Downtime per
Shift by machine type. Scatter plot: Energy per Unit vs. machine age (join
`install_date` from `dim_machine`, compute age as a calculated column).

**Page 4 — Maintenance**
Donut chart: Preventive vs Corrective cost split. Bar chart: maintenance cost
by plant. Table of top 20 highest-cost maintenance events.

## 5. A slicer set that makes the whole thing interactive

Add slicers for `dim_plant[plant_name]`, `dim_machine[machine_type]`, and
`dim_date[date]` (as a between-dates slicer) on every page, synced across
pages via **View → Sync Slicers**. That's what makes it read as an
"executive dashboard" rather than a set of static charts.

## Why a proxy OEE and not a rupee revenue figure

This dataset tracks physical output (units, kWh, minutes), not sales price,
so there's no legitimate revenue number to compute — inventing a rupee
figure per unit would just be a made-up number dressed up as data. If you
want a revenue view, the honest way to add it is to attach a real or
clearly-labeled-assumed price per product in `dim_product` and multiply
through; the model doesn't do that by default.
