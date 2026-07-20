# L&T Hazira Smart Manufacturing Analytics Platform

An end-to-end analytics project: synthetic manufacturing data → SQL warehouse
→ Python ETL → interactive dashboard → machine-learning failure model.

**First and most important thing to say about this project, including in an
interview:** the data is synthetic. L&T doesn't publish machine-level
production, energy, or downtime figures anywhere public, and nobody outside
the company has access to them. This dataset is built to be *statistically
realistic* — plausible plant layouts, machine types, shift patterns, and
failure dynamics modeled after how a heavy-fabrication and process-equipment
business like Hazira actually runs — but every number in it is generated,
not observed. Say this plainly if asked; presenting it as real operational
data would be misrepresentation, and it doesn't need to be real to
demonstrate the skills.

## What's actually in here

```
lt_hazira_platform/
├── etl/
│   ├── generate_data.py       # builds the synthetic dataset (25,200 production records)
│   └── load_to_sql.py         # cleans, validates, loads into SQLite
├── sql/
│   ├── schema.sql             # star schema: 5 dimensions + 2 fact tables
│   └── sample_queries.sql     # 6 analytical queries answering the target questions
├── ml/
│   └── train_failure_model.py # gradient-boosted failure risk model
├── app/
│   └── app.py                  # Streamlit exploration dashboard
├── powerbi/
│   └── POWERBI_GUIDE.md        # data model + DAX measures for a Power BI dashboard
└── data/                       # generated CSVs, SQLite DB, and trained model land here
```

## Running it end to end

```bash
pip install -r requirements.txt

# 1. Generate the synthetic dataset
python etl/generate_data.py

# 2. Load and validate into SQLite
python etl/load_to_sql.py

# 3. Train the failure-prediction model
python ml/train_failure_model.py

# 4. Launch the exploration dashboard
streamlit run app/app.py
```

For a Power BI version instead of (or alongside) the Streamlit app, see
`powerbi/POWERBI_GUIDE.md` — the star schema is already Power-BI-ready, since
that's what a star schema is for.

## The dataset

- **5 plants** (Hazira Heavy Engineering, Hazira Process Equipment, Hazira
  Modular Fabrication, Powai Precision Unit, Coimbatore Components Unit)
- **40 machines** (8 machine types per plant: CNC cutting, heavy press
  forming, welding robots, shot blasting, sub-arc welding, rolling mills,
  CNC machining centers, heat treatment furnaces)
- **3 shifts/day** over **210 days** = **25,200 production records**
- **546 maintenance events** (preventive and corrective)

Each machine has a simulated "wear index" that accumulates daily and resets
after a maintenance event, so failures aren't pure noise — they correlate
with wear, the way real equipment degradation does. That's what makes the ML
section below a genuine modeling exercise rather than fitting noise.

## The SQL layer

Normalized star schema: `dim_plant`, `dim_machine`, `dim_shift`,
`dim_product`, `dim_date` feeding `fact_production` and `fact_maintenance`,
with foreign keys and indexes on the join columns. `sql/sample_queries.sql`
has six queries answering exactly the kind of question this project was
scoped around — highest energy consumption by machine, production trend by
category, an OEE proxy, maintenance cost breakdown, failure rate by machine
type.

## The ETL

`load_to_sql.py` isn't a one-line `df.to_sql()` dump. It checks referential
integrity (every foreign key in the fact tables actually exists in its
dimension before loading), enforces sane bounds (downtime can't exceed an
8-hour shift, quantities can't be negative), and logs what it dropped and
why. That's the part of an ETL pipeline that actually matters in a real job,
more than the happy-path load itself.

## The ML model — and an honest result, not a polished one

The model predicts failure risk using only pre-shift information: prior wear
index, recent downtime history, machine specs. It deliberately excludes the
current shift's own downtime and defect numbers, because those are a
*consequence* of a failure event in this dataset's generation logic, not a
predictor of one — including them produced a fake ROC-AUC of 1.00 on the
first pass, which was a leakage bug, not a good model, and is called out
directly in the code comments and commit history rather than quietly fixed
and hidden.

With the leak removed, the honest number is **ROC-AUC ≈ 0.49** — no better
than random. That's a legitimate finding worth stating in an interview: with
only an aggregate wear index and no real condition-monitoring signal
(vibration, temperature, acoustic sensors), there isn't enough information
in this dataset to predict a rare event (1.45% of shifts) reliably. A
production version of this problem needs actual sensor telemetry, not
summary statistics. Knowing when a model *isn't* working, and being able to
explain precisely why, is worth more in an interview than a suspiciously
perfect AUC that nobody bothers to interrogate.

## The dashboard

Streamlit app with plant/machine-type/date filters, four tabs (Production &
Quality, Downtime & Energy, Maintenance, Failure Model), and a plain-language
answer to "which machine had the highest energy consumption" computed
directly from the filtered data — no LLM needed for a lookup like that; save
the LLM for the unstructured-document questions in the other project
(L&T Manufacturing Insights Assistant).

## Honest limitations, worth naming up front

- Synthetic data, not real L&T figures — said above, said again because it's
  the single most important caveat in this repo.
- No sensor telemetry, so the failure model's ceiling is low by design, not
  by mistake.
- No real product pricing, so there's no revenue figure — see the Power BI
  guide for why one isn't fabricated.
- Character-level chunking isn't used here (that's the other project); this
  one is all structured data, so that concern doesn't apply.

## Stack

Python · pandas · NumPy · SQLite (portable to PostgreSQL/MySQL/SQL Server
with minor type changes) · scikit-learn · Streamlit · Plotly · Power BI (via
the guide) · Git
