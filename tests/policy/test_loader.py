"""Tests for safe, deterministic YAML policy loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from aapp_mart.policy.loader import PolicyFileError, load_policy
from aapp_mart.policy.models import Policy


def _write_policy(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "policy.yml"
    path.write_text(content, encoding="utf-8")
    return path


def test_load_policy_reads_allowlists_as_frozensets(tmp_path: Path) -> None:
    path = _write_policy(
        tmp_path,
        """
allowed_targets:
  - staging.example.test
  - api.example.test
allowed_actions:
  - read_only_check
  - inventory
""",
    )

    policy = load_policy(path)

    assert policy == Policy(
        allowed_targets=frozenset({"staging.example.test", "api.example.test"}),
        allowed_actions=frozenset({"read_only_check", "inventory"}),
        enabled=True,
    )
    assert isinstance(policy.allowed_targets, frozenset)
    assert isinstance(policy.allowed_actions, frozenset)


def test_load_policy_defaults_enabled_to_true(tmp_path: Path) -> None:
    path = _write_policy(
        tmp_path,
        "allowed_targets: [staging.example.test]\n"
        "allowed_actions: [read_only_check]\n",
    )

    assert load_policy(path).enabled is True


def test_load_policy_preserves_explicit_disabled_state(tmp_path: Path) -> None:
    path = _write_policy(
        tmp_path,
        "enabled: false\n"
        "allowed_targets: [staging.example.test]\n"
        "allowed_actions: [read_only_check]\n",
    )

    assert load_policy(path).enabled is False


def test_load_policy_deduplicates_allowlist_entries(tmp_path: Path) -> None:
    path = _write_policy(
        tmp_path,
        "allowed_targets: [staging.example.test, staging.example.test]\n"
        "allowed_actions: [read_only_check, read_only_check]\n",
    )

    policy = load_policy(path)

    assert policy.allowed_targets == frozenset({"staging.example.test"})
    assert policy.allowed_actions == frozenset({"read_only_check"})


def test_load_policy_reports_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "missing.yml"

    with pytest.raises(PolicyFileError, match="Could not read policy file") as exc_info:
        load_policy(path)

    assert isinstance(exc_info.value.__cause__, OSError)


def test_load_policy_reports_directory_instead_of_file(tmp_path: Path) -> None:
    with pytest.raises(PolicyFileError, match="Could not read policy file"):
        load_policy(tmp_path)


def test_load_policy_rejects_invalid_utf8(tmp_path: Path) -> None:
    path = tmp_path / "policy.yml"
    path.write_bytes(b"allowed_targets: [\xff]\n")

    with pytest.raises(PolicyFileError, match="Could not read policy file"):
        load_policy(path)


def test_load_policy_rejects_malformed_yaml(tmp_path: Path) -> None:
    path = _write_policy(tmp_path, "allowed_targets: [\n")

    with pytest.raises(PolicyFileError, match="invalid YAML"):
        load_policy(path)


@pytest.mark.parametrize("content", ["[]\n", "null\n", "\n", "hello\n"])
def test_load_policy_requires_yaml_mapping(tmp_path: Path, content: str) -> None:
    path = _write_policy(tmp_path, content)

    with pytest.raises(PolicyFileError, match="YAML object"):
        load_policy(path)


def test_load_policy_rejects_unknown_fields(tmp_path: Path) -> None:
    path = _write_policy(
        tmp_path,
        "allowed_targets: [staging.example.test]\n"
        "allowed_actions: [read_only_check]\n"
        "unexpected: true\n",
    )

    with pytest.raises(PolicyFileError, match="Unknown policy field.*unexpected"):
        load_policy(path)


def test_load_policy_requires_boolean_enabled_value(tmp_path: Path) -> None:
    path = _write_policy(
        tmp_path,
        "enabled: 'false'\n"
        "allowed_targets: [staging.example.test]\n"
        "allowed_actions: [read_only_check]\n",
    )

    with pytest.raises(PolicyFileError, match="enabled.*boolean"):
        load_policy(path)


@pytest.mark.parametrize("key", ["allowed_targets", "allowed_actions"])
def test_load_policy_requires_each_allowlist_field(tmp_path: Path, key: str) -> None:
    content = (
        "allowed_actions: [read_only_check]\n"
        if key == "allowed_targets"
        else "allowed_targets: [staging.example.test]\n"
    )
    path = _write_policy(tmp_path, content)

    with pytest.raises(PolicyFileError, match=f"'{key}'.*list of strings"):
        load_policy(path)


@pytest.mark.parametrize("key", ["allowed_targets", "allowed_actions"])
def test_load_policy_rejects_non_list_allowlist(tmp_path: Path, key: str) -> None:
    other_key = "allowed_actions" if key == "allowed_targets" else "allowed_targets"
    other_value = "[read_only_check]" if other_key == "allowed_actions" else "[staging.example.test]"
    path = _write_policy(tmp_path, f"{key}: invalid\n{other_key}: {other_value}\n")

    with pytest.raises(PolicyFileError, match=f"'{key}'.*list of strings"):
        load_policy(path)


@pytest.mark.parametrize("key", ["allowed_targets", "allowed_actions"])
def test_load_policy_rejects_non_string_allowlist_items(tmp_path: Path, key: str) -> None:
    other_key = "allowed_actions" if key == "allowed_targets" else "allowed_targets"
    other_value = "[read_only_check]" if other_key == "allowed_actions" else "[staging.example.test]"
    path = _write_policy(tmp_path, f"{key}: [123]\n{other_key}: {other_value}\n")

    with pytest.raises(PolicyFileError, match=f"Every item in '{key}'.*string"):
        load_policy(path)


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("allowed_targets", "''", "must not be empty"),
        ("allowed_targets", "'*'", "Wildcard"),
        ("allowed_actions", "''", "must not be empty"),
        ("allowed_actions", "'*'", "Wildcard"),
    ],
)
def test_load_policy_validates_scope_values(
    tmp_path: Path,
    key: str,
    value: str,
    message: str,
) -> None:
    # The loader contract requires both allowlist fields to be YAML lists.
    # Keep the invalid scope value as a list item so validate_policy() is the
    # code path under test, rather than _read_string_list().
    targets = f"[{value}]" if key == "allowed_targets" else "[staging.example.test]"
    actions = f"[{value}]" if key == "allowed_actions" else "[read_only_check]"
    path = _write_policy(
        tmp_path,
        f"allowed_targets: {targets}\nallowed_actions: {actions}\n",
    )

    with pytest.raises(PolicyFileError, match=message):
        load_policy(path)
