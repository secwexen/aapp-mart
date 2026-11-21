"""Unit tests for the ENGINE execution pipeline."""

# pylint: disable=redefined-outer-name

from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, cast
from uuid import UUID, uuid4

import pytest

from aapp_mart.engine.contracts import (ComponentName, ExecutionComponent,
                                        ExecutionRequest, ExecutionResult,
                                        ExecutionStatus, new_contract_metadata)
from aapp_mart.engine.exceptions import (ComponentNotRegisteredError,
                                         ExecutionError)
from aapp_mart.engine.pipeline import ExecutionPipeline
from aapp_mart.engine.state_machine import StateTransition
from aapp_mart.events import EventPublisher


class MockComponent:  # pylint: disable=too-few-public-methods
    """Simple executable component for pipeline tests."""

    def __init__(
        self,
        component_name: ComponentName = ComponentName.AAPP,
        output: Mapping[str, Any] | None = None,
    ) -> None:
        """Initialize the mock component."""
        self.component_name = component_name
        self.output = dict(output or {"result": "success"})
        self.execution_count = 0
        self.should_raise = False
        self.return_invalid_result = False
        self.return_mismatched_id = False

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        """Execute a request and return a controlled result."""
        self.execution_count += 1

        if self.should_raise:
            raise RuntimeError("Component execution failed.")

        if self.return_invalid_result:
            return cast(ExecutionResult, "invalid result")

        execution_id = request.execution_id

        if self.return_mismatched_id:
            execution_id = uuid4()

        now = datetime.now(timezone.utc)

        return ExecutionResult(
            execution_id=execution_id,
            component=request.component,
            status=ExecutionStatus.SUCCEEDED,
            output=self.output,
            error=None,
            started_at=now,
            completed_at=now,
            metadata=request.metadata,
        )


def create_request(
    component: ComponentName = ComponentName.AAPP,
    execution_id: UUID | None = None,
) -> ExecutionRequest:
    """Create a valid execution request."""
    return ExecutionRequest(
        component=component,
        operation="predict",
        payload={"subject": "test-subject"},
        metadata=new_contract_metadata(),
        execution_id=execution_id or uuid4(),
    )


@pytest.fixture
def pipeline_fixture() -> ExecutionPipeline:
    """Create an execution pipeline."""
    return ExecutionPipeline()


@pytest.fixture
def component_fixture() -> MockComponent:
    """Create a mock AAPP component."""
    return MockComponent()


class TestExecutionPipelineInitialization:
    """Tests for pipeline initialization."""

    def test_pipeline_starts_without_registered_components(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that no components are registered initially."""
        assert pipeline_fixture.registered_components == ()

    def test_pipeline_creates_event_publisher(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that the pipeline has an event publisher."""
        assert pipeline_fixture.event_publisher is not None

    def test_pipeline_uses_injected_event_publisher(self) -> None:
        """Verify that an injected publisher is preserved."""
        publisher = EventPublisher()
        execution_pipeline = ExecutionPipeline(event_publisher=publisher)

        assert execution_pipeline.event_publisher is publisher


class TestComponentRegistration:
    """Tests for component registration and removal."""

    def test_register_component(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that a component can be registered."""
        pipeline_fixture.register_component(component_fixture)

        assert ComponentName.AAPP in pipeline_fixture.registered_components

    def test_register_multiple_components(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that multiple components can be registered."""
        aapp = MockComponent(ComponentName.AAPP)
        mart = MockComponent(ComponentName.MART)
        engine = MockComponent(ComponentName.ENGINE)

        pipeline_fixture.register_component(aapp)
        pipeline_fixture.register_component(mart)
        pipeline_fixture.register_component(engine)

        assert pipeline_fixture.registered_components == (
            ComponentName.AAPP,
            ComponentName.MART,
            ComponentName.ENGINE,
        )

    def test_register_duplicate_component_raises_error(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that duplicate registration is rejected."""
        pipeline_fixture.register_component(component_fixture)

        with pytest.raises(ValueError, match="Component already registered"):
            pipeline_fixture.register_component(MockComponent())

    def test_replace_existing_component(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that an existing component can be replaced."""
        original = MockComponent(output={"version": "original"})
        replacement = MockComponent(output={"version": "replacement"})

        pipeline_fixture.register_component(original)
        pipeline_fixture.register_component(
            replacement,
            replace_existing=True,
        )

        result = pipeline_fixture.submit(create_request())

        assert original.execution_count == 0
        assert replacement.execution_count == 1
        assert result.output == {"version": "replacement"}

    def test_invalid_component_name_is_rejected(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that components with invalid names are rejected."""

        class InvalidComponent: # pylint: disable=too-few-public-methods
            """Component with an invalid component name."""

            component_name = "AAPP"

            def execute(self, request: ExecutionRequest) -> ExecutionResult:
                """Reject execution for this invalid component."""
                del request
                raise NotImplementedError

        invalid_component = cast(
            ExecutionComponent,
            InvalidComponent(),
        )

        with pytest.raises(TypeError, match="valid component_name"):
            pipeline_fixture.register_component(invalid_component)

    def test_component_without_execute_is_rejected(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that components without execute are rejected."""

        class InvalidComponent: # pylint: disable=too-few-public-methods
            """Component that does not implement execute."""

            component_name = ComponentName.AAPP

        invalid_component = cast(
            ExecutionComponent,
            InvalidComponent(),
        )

        with pytest.raises(TypeError, match=r"implement execute"):
            pipeline_fixture.register_component(invalid_component)

    def test_unregister_existing_component(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that a registered component can be removed."""
        pipeline_fixture.register_component(component_fixture)

        result = pipeline_fixture.unregister_component(ComponentName.AAPP)

        assert result is True
        assert ComponentName.AAPP not in pipeline_fixture.registered_components

    def test_unregister_missing_component_returns_false(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that removing an unknown component returns False."""
        result = pipeline_fixture.unregister_component(ComponentName.MART)

        assert result is False


class TestExecutionSubmission:
    """Tests for execution request submission."""

    def test_submit_successful_execution(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that a valid request executes successfully."""
        pipeline_fixture.register_component(component_fixture)

        request = create_request()
        result = pipeline_fixture.submit(request)

        assert result.execution_id == request.execution_id
        assert result.component == ComponentName.AAPP
        assert result.status == ExecutionStatus.SUCCEEDED
        assert result.output == {"result": "success"}
        assert component_fixture.execution_count == 1

    def test_submit_routes_to_correct_component(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that requests are routed to their registered components."""
        aapp = MockComponent(
            ComponentName.AAPP,
            {"component": "aapp"},
        )
        mart = MockComponent(
            ComponentName.MART,
            {"component": "mart"},
        )

        pipeline_fixture.register_component(aapp)
        pipeline_fixture.register_component(mart)

        result = pipeline_fixture.submit(create_request(ComponentName.MART))

        assert result.component == ComponentName.MART
        assert result.output == {"component": "mart"}
        assert aapp.execution_count == 0
        assert mart.execution_count == 1

    def test_submit_unregistered_component_raises_error(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that unregistered components cannot execute."""
        request = create_request(ComponentName.MART)

        with pytest.raises(
            ComponentNotRegisteredError,
            match="Component is not registered",
        ):
            pipeline_fixture.submit(request)

    def test_submit_duplicate_execution_id_raises_error(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that an execution ID cannot be submitted twice."""
        pipeline_fixture.register_component(component_fixture)
        request = create_request()

        pipeline_fixture.submit(request)

        with pytest.raises(
            ExecutionError,
            match="already been submitted",
        ):
            pipeline_fixture.submit(request)

        assert component_fixture.execution_count == 1

    def test_component_exception_returns_failed_result(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that component exceptions produce failed executions."""
        mock_component = MockComponent()
        mock_component.should_raise = True
        pipeline_fixture.register_component(mock_component)

        result = pipeline_fixture.submit(create_request())

        assert result.status == ExecutionStatus.FAILED
        assert result.error is not None
        assert result.error["type"] == "RuntimeError"

    def test_invalid_component_result_returns_failed_result(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that invalid component results fail the execution."""
        mock_component = MockComponent()
        mock_component.return_invalid_result = True
        pipeline_fixture.register_component(mock_component)

        result = pipeline_fixture.submit(create_request())

        assert result.status == ExecutionStatus.FAILED
        assert result.error is not None
        assert result.error["type"] == "TypeError"

    def test_mismatched_execution_id_returns_failed_result(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that mismatched result IDs fail the execution."""
        mock_component = MockComponent()
        mock_component.return_mismatched_id = True
        pipeline_fixture.register_component(mock_component)

        result = pipeline_fixture.submit(create_request())

        assert result.status == ExecutionStatus.FAILED
        assert result.error is not None


class TestExecutionStateTracking:
    """Tests for execution state and history tracking."""

    def test_get_state_after_successful_execution(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that successful execution state is retained."""
        pipeline_fixture.register_component(component_fixture)
        request = create_request()

        pipeline_fixture.submit(request)

        assert pipeline_fixture.get_state(request.execution_id) == ExecutionStatus.SUCCEEDED

    def test_get_state_after_failed_execution(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that failed execution state is retained."""
        mock_component = MockComponent()
        mock_component.should_raise = True
        pipeline_fixture.register_component(mock_component)

        request = create_request()
        pipeline_fixture.submit(request)

        assert pipeline_fixture.get_state(request.execution_id) == ExecutionStatus.FAILED

    def test_get_state_history_returns_transitions(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that execution transitions are retained."""
        pipeline_fixture.register_component(component_fixture)
        request = create_request()

        pipeline_fixture.submit(request)

        history = pipeline_fixture.get_state_history(request.execution_id)

        assert isinstance(history, tuple)
        assert len(history) == 2
        assert all(isinstance(entry, StateTransition) for entry in history)
        assert [entry.current for entry in history] == [
            ExecutionStatus.RUNNING,
            ExecutionStatus.SUCCEEDED,
        ]

    def test_get_state_for_unknown_execution_raises_error(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that unknown execution state lookup fails."""
        execution_id = uuid4()

        with pytest.raises(
            ExecutionError,
            match="Execution state not found",
        ):
            pipeline_fixture.get_state(execution_id)

    def test_get_history_for_unknown_execution_raises_error(
        self,
        pipeline_fixture: ExecutionPipeline,
    ) -> None:
        """Verify that unknown execution history lookup fails."""
        execution_id = uuid4()

        with pytest.raises(
            ExecutionError,
            match="Execution state not found",
        ):
            pipeline_fixture.get_state_history(execution_id)


class TestExecutionPipelineConcurrency:
    """Tests for pipeline concurrency behavior."""

    def test_concurrent_submissions_use_unique_execution_ids(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that independent concurrent submissions succeed."""
        pipeline_fixture.register_component(component_fixture)

        requests = [create_request() for _ in range(20)]

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(pipeline_fixture.submit, requests))

        assert len(results) == 20
        assert all(result.status == ExecutionStatus.SUCCEEDED for result in results)
        assert component_fixture.execution_count == 20

    def test_concurrent_duplicate_submission_is_rejected(
        self,
        pipeline_fixture: ExecutionPipeline,
        component_fixture: MockComponent,
    ) -> None:
        """Verify that duplicate IDs cannot be submitted concurrently."""
        pipeline_fixture.register_component(component_fixture)
        request = create_request()

        def submit_request(_: int) -> str:
            """Submit the shared request and report its outcome."""
            try:
                pipeline_fixture.submit(request)
                return "success"
            except ExecutionError:
                return "duplicate"

        with ThreadPoolExecutor(max_workers=8) as executor:
            outcomes = list(executor.map(submit_request, range(8)))

        assert outcomes.count("success") == 1
        assert outcomes.count("duplicate") == 7
        assert component_fixture.execution_count == 1
