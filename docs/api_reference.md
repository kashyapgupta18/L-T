# REST API Reference

The platform provides a FastAPI REST service:
- `GET /health`: Liveness probe and uptime tracking.
- `POST /predictions/risk`: Pre-shift failure risk score and triage action.
- `GET /analytics/oee-summary`: Aggregated plant OEE metrics.
- `GET /machines`: Equipment asset master data inventory.
