"""AAPP-MART orchestration for the Community Edition."""

from collections.abc import Mapping
from typing import Any, cast

from aapp_mart.aapp.models import PredictionMode
from aapp_mart.aapp.prediction import Prediction
from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    PredictionRequest,
    PredictionResult,
    SimulationRequest,
    SimulationResult,
)
from aapp_mart.engine.utils import derive_seed, normalize_error, utc_now
from aapp_mart.simulation.simulator import Simulator


# pylint: disable=too-few-public-methods
class AAPPMartOrchestrator:
    """Coordinate AAPP prediction and MART simulation.

    The single public execute method is intentional: the orchestrator
    implements the ENGINE execution-component contract.
    """

    component_name = ComponentName.ENGINE

    def __init__(
        self,
        prediction: Prediction,
        simulator: Simulator,
    ) -> None:
        """Initialize the orchestrator with AAPP and MART components."""

        self._prediction = prediction
        self._simulator = simulator

    @staticmethod
    def _require_mapping(
        value: object,
        field_name: str,
    ) -> Mapping[str, Any]:
        """Validate a mapping field in the execution payload."""

        if not isinstance(value, Mapping):
            raise ValueError(f"'{field_name}' must be a mapping.")

        typed_value = cast(Mapping[object, object], value)

        if not all(isinstance(key, str) for key in typed_value):
            raise ValueError(f"'{field_name}' must contain string keys.")

        return cast(Mapping[str, Any], value)

    @staticmethod
    def _require_string(
        value: object,
        field_name: str,
    ) -> str:
        """Validate a required non-empty string field."""

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"'{field_name}' must be a non-empty string.")

        return value

    @staticmethod
    def _optional_string(
        value: object,
        field_name: str,
    ) -> str | None:
        """Validate an optional string field."""

        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError(f"'{field_name}' must be a string or None.")

        return value

    @staticmethod
    def _serialize_prediction(
        result: PredictionResult,
    ) -> dict[str, Any]:
        """Convert a prediction result into a serializable mapping."""

        return {
            "subject": result.subject,
            "predicted_paths": result.predicted_paths,
            "confidence": result.confidence,
            "rationale": result.rationale,
        }

    @staticmethod
    def _serialize_simulation(
        result: SimulationResult,
    ) -> dict[str, Any]:
        """Convert a simulation result into a serializable mapping."""

        return {
            "scenario": result.scenario,
            "events": result.events,
            "summary": result.summary,
            "started_at": result.started_at,
            "completed_at": result.completed_at,
        }

    @staticmethod
    def _derive_component_seeds(
        request: ExecutionRequest,
    ) -> tuple[int | None, int | None]:
        """Derive independent reproducible seeds for AAPP and MART."""

        if not request.deterministic:
            return None, None

        if request.seed is None:
            raise ValueError("A deterministic execution requires a seed.")

        return (
            derive_seed(request.seed, "aapp-prediction"),
            derive_seed(request.seed, "mart-simulation"),
        )

    def _run_prediction(
        self,
        request: ExecutionRequest,
        payload: Mapping[str, Any],
        seed: int | None,
    ) -> PredictionResult:
        """Build and execute the AAPP prediction request."""

        prediction_mode_value = self._require_string(
            payload.get(
                "mode",
                PredictionMode.DETERMINISTIC.value,
            ),
            "prediction.mode",
        )
        prediction_mode = PredictionMode(prediction_mode_value)

        prediction_request = PredictionRequest(
            subject=self._require_string(
                payload.get("subject"),
                "prediction.subject",
            ),
            features=self._require_mapping(
                payload.get("features"),
                "prediction.features",
            ),
            objective=self._require_string(
                payload.get("objective"),
                "prediction.objective",
            ),
            metadata=request.metadata,
            model_name=self._optional_string(
                payload.get("model_name"),
                "prediction.model_name",
            ),
            deterministic=request.deterministic,
            seed=seed,
        )

        return self._prediction.predict(
            prediction_request,
            mode=prediction_mode,
        )

    def _build_simulation_request(
        self,
        request: ExecutionRequest,
        payload: Mapping[str, Any],
        prediction_result: PredictionResult,
        seed: int | None,
    ) -> SimulationRequest:
        """Build the MART simulation request using AAPP output."""

        simulation_parameters = dict(
            self._require_mapping(
                payload.get("parameters", {}),
                "simulation.parameters",
            )
        )

        simulation_parameters["aapp_prediction"] = self._serialize_prediction(prediction_result)

        return SimulationRequest(
            scenario=self._require_string(
                payload.get("scenario"),
                "simulation.scenario",
            ),
            target=self._require_string(
                payload.get("target"),
                "simulation.target",
            ),
            parameters=simulation_parameters,
            metadata=request.metadata,
            seed=seed,
            deterministic=request.deterministic,
        )

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Execute AAPP prediction followed by MART simulation."""

        started_at = utc_now()
        stage = "validation"

        try:
            if request.component is not ComponentName.ENGINE:
                raise ValueError("Orchestrator requires the ENGINE component.")

            if request.operation != "predict_and_simulate":
                raise ValueError("Unsupported operation. Expected 'predict_and_simulate'.")

            payload = self._require_mapping(
                request.payload,
                "payload",
            )
            prediction_payload = self._require_mapping(
                payload.get("prediction"),
                "prediction",
            )
            simulation_payload = self._require_mapping(
                payload.get("simulation"),
                "simulation",
            )

            prediction_seed, simulation_seed = self._derive_component_seeds(request)

            stage = "aapp_prediction"
            prediction_result = self._run_prediction(
                request,
                prediction_payload,
                prediction_seed,
            )

            stage = "mart_simulation"
            simulation_request = self._build_simulation_request(
                request,
                simulation_payload,
                prediction_result,
                simulation_seed,
            )
            simulation_result = self._simulator.simulate(
                simulation_request,
            )

            completed_at = utc_now()

            return ExecutionResult(
                execution_id=request.execution_id,
                component=ComponentName.ENGINE,
                status=ExecutionStatus.SUCCEEDED,
                output={
                    "prediction": self._serialize_prediction(
                        prediction_result,
                    ),
                    "simulation": self._serialize_simulation(
                        simulation_result,
                    ),
                },
                started_at=started_at,
                completed_at=completed_at,
                metadata=request.metadata,
            )

        except Exception as error:  # pylint: disable=broad-exception-caught
            completed_at = utc_now()
            normalized_error = normalize_error(error)
            normalized_error["stage"] = stage

            return ExecutionResult(
                execution_id=request.execution_id,
                component=ComponentName.ENGINE,
                status=ExecutionStatus.FAILED,
                error=normalized_error,
                started_at=started_at,
                completed_at=completed_at,
                metadata=request.metadata,
            )


__all__ = ["AAPPMartOrchestrator"]
