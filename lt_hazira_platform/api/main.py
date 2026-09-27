"""FastAPI application entrypoint for L&T Hazira Analytics."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lt_hazira_platform.api.routes import health, predictions, analytics, machines
from lt_hazira_platform.api.middleware import RequestTimingMiddleware

app = FastAPI(
    title="L&T Hazira Manufacturing Analytics API",
    description="Operational telemetry, OEE metrics, and predictive failure risk service.",
    version="1.0.0"
)

app.add_middleware(RequestTimingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(predictions.router)
app.include_router(analytics.router)
app.include_router(machines.router)
