"""API routes for AAPP prediction."""

from fastapi import APIRouter

from aapp_mart.api.schemas import PredictionRequestSchema, PredictionResponseSchema

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "/",
    response_model=PredictionResponseSchema,
    status_code=200,
)
async def create_prediction(
    request: PredictionRequestSchema,
) -> PredictionResponseSchema:
    """Accept an AAPP prediction request.

    The AAPP execution integration will be implemented in a
    subsequent development step.
    """
    raise NotImplementedError("AAPP prediction integration has not been implemented yet.")


__all__ = ["router"]
