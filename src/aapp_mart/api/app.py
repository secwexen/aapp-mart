"""AAPP-MART API application entry point."""

from fastapi import FastAPI

from aapp_mart.api.routes.attack_graph import router as attack_graph_router
from aapp_mart.api.routes.prediction import router as prediction_router
from aapp_mart.api.routes.reports import router as reports_router
from aapp_mart.api.routes.risk import router as risk_router
from aapp_mart.api.routes.simulation import router as simulation_router

app = FastAPI(
    title="AAPP-MART Community Edition",
    description=(
        "Cybersecurity engine for attack path prediction, "
        "multi-agent red team simulation, and security risk assessment."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(prediction_router)
app.include_router(simulation_router)
app.include_router(risk_router)
app.include_router(reports_router)
app.include_router(attack_graph_router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return the application health status."""
    return {
        "status": "ok",
        "service": "aapp-mart",
    }


__all__ = ["app"]
