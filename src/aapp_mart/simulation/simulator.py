"""Simulation execution module."""

from collections.abc import Mapping
from datetime import datetime, timezone
from secrets import randbits
from typing import Any, Protocol, cast

from aapp_mart.engine.contracts import (
    ComponentName,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    MARTInterface,
    SimulationRequest,
    SimulationResult,
)
from aapp_mart.engine.utils import derive_seed
from aapp_mart.simulation.registry import SimulationScenarioRegistry
from aapp_mart.simulation.scenario import SimulationScenario
from aapp_mart.simulation.state import SimulationState
from aapp_mart.simulation.step import SimulationStep


class SimulationStepExecutor(Protocol):  # pylint: disable=too-few-public-methods
    """Define the interface for executing simulation steps."""

    def execute_step(
        self,
        scenario: SimulationScenario,
        step: SimulationStep,
        request: SimulationRequest,
        step_seed: int,
    ) -> Mapping[str, Any]:
        """Execute a step and return its actual execution event."""
        ...


class Simulator(MARTInterface):
    """Coordinate simulation scenario execution."""

    def __init__(
        self,
        registry: SimulationScenarioRegistry,
        step_executor: SimulationStepExecutor,
    ) -> None:
        """Initialize the simulator dependencies."""
        self._registry = registry
        self._step_executor = step_executor
        self._state = SimulationState.PENDING

    @property
    def state(self) -> SimulationState:
        """Return the current simulation lifecycle state."""
        return self._state

    @property
    def component_name(self) -> ComponentName:
        """Return the ENGINE component identifier."""
        return ComponentName.MART

    def validate_scenario(
        self,
        scenario: SimulationScenario,
        steps: tuple[SimulationStep, ...],
    ) -> None:
        """Validate a scenario before execution."""
        if not scenario.scenario_id.strip():
            raise ValueError("Scenario ID cannot be empty.")

        step_ids = [step.step_id for step in steps]

        if len(step_ids) != len(set(step_ids)):
            raise ValueError("Duplicate simulation step IDs.")

    def _execute_steps(
        self,
        scenario: SimulationScenario,
        steps: tuple[SimulationStep, ...],
        request: SimulationRequest,
    ) -> tuple[Mapping[str, Any], ...]:
        """Execute scenario steps and collect actual events."""
        self.validate_scenario(scenario, steps)

        events: list[Mapping[str, Any]] = []

        if request.deterministic:
            if request.seed is None:
                raise ValueError("Deterministic simulation requires a seed.")
            base_seed = request.seed
        else:
            base_seed = randbits(64)

        for step in steps:
            step_seed = derive_seed(
                base_seed,
                f"{scenario.scenario_id}:{step.step_id}",
            )

            event = self._step_executor.execute_step(
                scenario,
                step,
                request,
                step_seed,
            )

            events.append(dict(event))

        return tuple(events)

    def simulate(
        self,
        request: SimulationRequest,
    ) -> SimulationResult:
        """Execute a registered scenario and return its results."""
        started_at = datetime.now(timezone.utc)
        self._state = SimulationState.RUNNING

        try:
            scenario = self._registry.get(request.scenario)

            self.validate_scenario(
                scenario,
                scenario.steps,
            )

            events = self._execute_steps(
                scenario,
                scenario.steps,
                request,
            )

            completed_at = datetime.now(timezone.utc)
            self._state = SimulationState.COMPLETED

            return SimulationResult(
                scenario=scenario.scenario_id,
                events=events,
                summary={
                    "state": self._state.value,
                    "total_steps": len(scenario.steps),
                    "completed_steps": len(events),
                },
                started_at=started_at,
                completed_at=completed_at,
                metadata=request.metadata,
            )

        except Exception:  # pylint: disable=broad-exception-caught
            self._state = SimulationState.FAILED
            raise

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        """Execute MART simulation through the ENGINE contract."""
        started_at = datetime.now(timezone.utc)

        try:
            if request.component != ComponentName.MART:
                raise ValueError("Execution request component must be MART.")

            if request.operation != "simulate":
                raise ValueError("Unsupported MART operation.")

            simulation_request = self._build_simulation_request(request)
            result = self.simulate(simulation_request)

            return ExecutionResult(
                execution_id=request.execution_id,
                component=ComponentName.MART,
                status=ExecutionStatus.SUCCEEDED,
                output={
                    "scenario": result.scenario,
                    "events": result.events,
                    "summary": result.summary,
                },
                started_at=started_at,
                completed_at=datetime.now(timezone.utc),
                metadata=request.metadata,
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            return ExecutionResult(
                execution_id=request.execution_id,
                component=ComponentName.MART,
                status=ExecutionStatus.FAILED,
                error={
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
                started_at=started_at,
                completed_at=datetime.now(timezone.utc),
                metadata=request.metadata,
            )

    @staticmethod
    def _build_simulation_request(
        request: ExecutionRequest,
    ) -> SimulationRequest:
        """Build a domain simulation request from an ENGINE request."""
        payload = request.payload

        scenario = payload.get("scenario")
        target = payload.get("target")
        parameters = payload.get("parameters", {})

        if not isinstance(scenario, str):
            raise ValueError("MART simulation scenario must be a string.")

        if not isinstance(target, str):
            raise ValueError("MART simulation target must be a string.")

        if not isinstance(parameters, Mapping):
            raise ValueError("MART simulation parameters must be a mapping.")

        typed_parameters = cast(Mapping[str, Any], parameters)

        return SimulationRequest(
            scenario=scenario,
            target=target,
            parameters=typed_parameters,
            metadata=request.metadata,
            seed=request.seed,
            deterministic=request.deterministic,
        )
