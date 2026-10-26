# Data Dictionary

## Dimensions
- `dim_plant`: Facility locations (Hazira Heavy Engineering, Hazira Modular Fabrication, etc.)
- `dim_machine`: 40 machine assets across 8 equipment classifications.
- `dim_shift`: 3 eight-hour shifts per day (Morning, Evening, Night).
- `dim_product`: Fabricated industrial components and process assemblies.
- `dim_date`: Temporal calendar attributes covering 210 simulation days.

## Fact Tables
- `fact_production`: 25,200 shift production records containing units, defects, uptime, energy, and wear index.
- `fact_maintenance`: 546 corrective and preventive maintenance events with labor/parts cost breakdown.
