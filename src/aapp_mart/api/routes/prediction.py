"""API routes for AAPP prediction."""

from fastapi import APIRouter, HTTPException, Request

from aapp_mart.api.schemas import ExecutionResponseSchema, PredictionRequestSchema
from aapp_mart.engine.contracts import ComponentName, ExecutionRequest, new_contract_metadata
from aapp_mart.engine.exceptions import ComponentNotRegisteredError, ContractValidationError, ExecutionError
from aapp_mart.engine.pipeline import ExecutionPipeline

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "/",
    response_model=ExecutionResponseSchema,
    status_code=200,
)
async def create_prediction(
    request: PredictionRequestSchema,
    http_request: Request,
) -> ExecutionResponseSchema:
    """Execute an AAPP prediction through the ENGINE pipeline."""
    pipeline: ExecutionPipeline | None = getattr(
        http_request.app.state,
        "execution_pipeline",
        None,
    )

    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "execution_pipeline_unavailable",
                "message": "The execution pipeline is not available.",
            },
        )

    try:
        execution_request = ExecutionRequest(
            component=ComponentName.AAPP,
            operation="predict",
            payload=request.model_dump(),
            metadata=new_contract_metadata(),
            deterministic=request.deterministic,
            seed=request.seed,
        )

        result = pipeline.submit(execution_request)

        return ExecutionResponseSchema.model_validate(result)

    except ContractValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "invalid_execution_request",
                "message": str(exc),
            },
        ) from exc

    except ComponentNotRegisteredError as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "component_unavailable",
                "message": str(exc),
            },
        ) from exc

    except ExecutionError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "execution_conflict",
                "message": str(exc),
            },
        ) from exc


__all__ = ["router"]
