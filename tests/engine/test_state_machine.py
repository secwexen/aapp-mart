"""Unit tests for the ENGINE execution state machine."""

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

import pytest

from aapp_mart.engine.contracts import ExecutionStatus
from aapp_mart.engine.state_machine import ExecutionStateMachine, StateTransition

# Pytest fixtures are intentionally used as test function parameters.
# pylint: disable=redefined-outer-name


@pytest.fixture
def state_machine() -> ExecutionStateMachine:
    """Create a fresh execution state machine."""
    return ExecutionStateMachine()


class TestExecutionStateMachineInitialization:
    """Tests for state machine initialization."""

    def test_initial_state_is_pending(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that the initial state is PENDING."""
        assert state_machine.status == ExecutionStatus.PENDING

    def test_initial_history_is_empty(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that history contains only actual transitions."""
        assert state_machine.history == ()

    def test_initial_state_is_not_terminal(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that a newly created state machine is not terminal."""
        assert not state_machine.is_terminal


class TestExecutionStateTransitions:
    """Tests for valid execution state transitions."""

    @pytest.mark.parametrize(
        "target_state",
        [
            ExecutionStatus.RUNNING,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        ],
    )
    def test_pending_state_allows_valid_transitions(
        self,
        state_machine: ExecutionStateMachine,
        target_state: ExecutionStatus,
    ) -> None:
        """Verify valid transitions from PENDING."""
        state_machine.transition(target_state)

        assert state_machine.status == target_state

    @pytest.mark.parametrize(
        "target_state",
        [
            ExecutionStatus.SUCCEEDED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        ],
    )
    def test_running_state_allows_terminal_transitions(
        self,
        state_machine: ExecutionStateMachine,
        target_state: ExecutionStatus,
    ) -> None:
        """Verify valid terminal transitions from RUNNING."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(target_state)

        assert state_machine.status == target_state

    def test_pending_to_running_to_succeeded(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify the successful execution lifecycle."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(ExecutionStatus.SUCCEEDED)

        assert state_machine.status == ExecutionStatus.SUCCEEDED
        assert state_machine.is_terminal

    def test_pending_to_running_to_failed(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify the failed execution lifecycle."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(ExecutionStatus.FAILED)

        assert state_machine.status == ExecutionStatus.FAILED
        assert state_machine.is_terminal

    def test_pending_to_running_to_cancelled(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify the cancelled execution lifecycle."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(ExecutionStatus.CANCELLED)

        assert state_machine.status == ExecutionStatus.CANCELLED
        assert state_machine.is_terminal


class TestInvalidExecutionStateTransitions:
    """Tests for rejected execution state transitions."""

    @pytest.mark.parametrize(
        "target_state",
        [
            ExecutionStatus.PENDING,
            ExecutionStatus.SUCCEEDED,
        ],
    )
    def test_pending_rejects_invalid_transitions(
        self,
        state_machine: ExecutionStateMachine,
        target_state: ExecutionStatus,
    ) -> None:
        """Verify that invalid transitions from PENDING are rejected."""
        with pytest.raises(ValueError, match="Invalid execution transition"):
            state_machine.transition(target_state)

    def test_running_cannot_transition_back_to_pending(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that RUNNING cannot transition back to PENDING."""
        state_machine.transition(ExecutionStatus.RUNNING)

        with pytest.raises(ValueError, match="Invalid execution transition"):
            state_machine.transition(ExecutionStatus.PENDING)

    @pytest.mark.parametrize(
        "terminal_state",
        [
            ExecutionStatus.SUCCEEDED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        ],
    )
    def test_terminal_state_rejects_further_transitions(
        self,
        state_machine: ExecutionStateMachine,
        terminal_state: ExecutionStatus,
    ) -> None:
        """Verify that terminal states reject further transitions."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(terminal_state)

        with pytest.raises(ValueError, match="Invalid execution transition"):
            state_machine.transition(ExecutionStatus.RUNNING)

    def test_terminal_state_cannot_transition_to_another_terminal_state(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that terminal states cannot transition to each other."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(ExecutionStatus.SUCCEEDED)

        with pytest.raises(ValueError, match="Invalid execution transition"):
            state_machine.transition(ExecutionStatus.FAILED)


class TestExecutionStateHistory:
    """Tests for execution state history."""

    def test_history_records_each_transition(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that every successful transition is recorded."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(ExecutionStatus.SUCCEEDED)

        history = state_machine.history

        assert len(history) == 2
        assert [entry.previous for entry in history] == [
            ExecutionStatus.PENDING,
            ExecutionStatus.RUNNING,
        ]
        assert [entry.current for entry in history] == [
            ExecutionStatus.RUNNING,
            ExecutionStatus.SUCCEEDED,
        ]

    def test_transition_returns_transition_record(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that transition returns its recorded transition."""
        transition = state_machine.transition(ExecutionStatus.RUNNING)

        assert transition.previous == ExecutionStatus.PENDING
        assert transition.current == ExecutionStatus.RUNNING
        assert transition in state_machine.history

    def test_history_timestamps_are_timezone_aware(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that transition timestamps are timezone-aware."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(ExecutionStatus.SUCCEEDED)

        for entry in state_machine.history:
            assert entry.timestamp.tzinfo is not None
            assert entry.timestamp.utcoffset() is not None

    def test_history_timestamps_are_monotonic(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that history timestamps are ordered."""
        state_machine.transition(ExecutionStatus.RUNNING)
        state_machine.transition(ExecutionStatus.SUCCEEDED)

        timestamps = [entry.timestamp for entry in state_machine.history]

        assert timestamps == sorted(timestamps)

    def test_history_returns_immutable_snapshot(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that history is exposed as an immutable tuple."""
        state_machine.transition(ExecutionStatus.RUNNING)

        assert isinstance(state_machine.history, tuple)

    def test_history_snapshot_does_not_change_after_transition(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify that previous history snapshots remain unchanged."""
        state_machine.transition(ExecutionStatus.RUNNING)
        initial_history = state_machine.history

        state_machine.transition(ExecutionStatus.SUCCEEDED)

        assert len(initial_history) == 1
        assert initial_history[0].current == ExecutionStatus.RUNNING
        assert len(state_machine.history) == 2


class TestExecutionStateMachineConcurrency:
    """Tests for thread-safe state machine access."""

    def test_concurrent_state_reads_are_consistent(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify consistent state reads across multiple threads."""
        state_machine.transition(ExecutionStatus.RUNNING)

        def read_state(_: int) -> ExecutionStatus:
            """Read the current execution state."""
            return state_machine.status

        reader: Callable[[int], ExecutionStatus] = read_state

        with ThreadPoolExecutor(max_workers=8) as executor:
            states = list(executor.map(reader, range(100)))

        assert all(state == ExecutionStatus.RUNNING for state in states)

    def test_concurrent_history_reads_are_consistent(
        self,
        state_machine: ExecutionStateMachine,
    ) -> None:
        """Verify consistent history reads across multiple threads."""
        state_machine.transition(ExecutionStatus.RUNNING)

        def read_history(_: int) -> tuple[StateTransition, ...]:
            """Read the current execution history."""
            return state_machine.history

        reader: Callable[
            [int],
            tuple[StateTransition, ...],
        ] = read_history

        with ThreadPoolExecutor(max_workers=8) as executor:
            histories = list(executor.map(reader, range(100)))

        assert all(history[-1].current == ExecutionStatus.RUNNING for history in histories)
