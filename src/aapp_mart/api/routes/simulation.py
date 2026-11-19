"""API routes for MART simulation."""

from fastapi import APIRouter

from aapp_mart.api.schemas import SimulationRequestSchema, SimulationResponseSchema

router = APIRouter(
    prefix="/simulations",
    tags=["Simulations"],
)


@router.post(
    "/",
    response_model=SimulationResponseSchema,
    status_code=200,
)
async def create_simulation(
    request: SimulationRequestSchema,
) -> SimulationResponseSchema:
    """Accept a MART simulation request.

    The MART execution integration will be implemented in a
    subsequent development step.
    """
    raise NotImplementedError("MART simulation integration has not been implemented yet.")


__all__ = ["router"]
