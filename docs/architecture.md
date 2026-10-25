# System Architecture

The L&T Hazira Smart Manufacturing Analytics Platform is structured into modular layers:

1. **Storage Layer**: SQLite analytical warehouse with normalized star schema.
2. **ETL Layer**: Synthetic generation, physical validation, chunked batch loading.
3. **Analytics Layer**: Industrial OEE calculations, downtime Pareto, and MTBF/MTTR metrics.
4. **Machine Learning Layer**: Pre-shift leakage-free failure risk prediction.
5. **Presentation Layer**: Streamlit exploration UI and FastAPI REST microservice.
