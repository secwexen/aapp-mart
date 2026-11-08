import pytest

from aapp_mart.shared import (
    DEFAULT_ENCODING,
    DEFAULT_RETRY_COUNT,
    DEFAULT_TIMEOUT_SECONDS,
    flatten,
    normalize_name,
    require_list,
    require_mapping,
    require_non_empty_string,
)


def test_normalize_name() -> None:
    assert normalize_name("  Example Name  ", field_name="name") == "example name"


def test_normalize_name_rejects_empty() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        normalize_name("   ", field_name="name")


def test_require_non_empty_string() -> None:
    assert require_non_empty_string("  hello  ", "label") == "hello"


def test_require_mapping() -> None:
    assert require_mapping({"a": 1}, "payload") == {"a": 1}


def test_require_list() -> None:
    assert require_list([1, 2, 3], "items") == [1, 2, 3]


def test_flatten() -> None:
    assert flatten([[1, 2], [3], [4, 5]]) == [1, 2, 3, 4, 5]


def test_constants_are_exposed() -> None:
    assert DEFAULT_TIMEOUT_SECONDS > 0
    assert DEFAULT_RETRY_COUNT > 0
    assert DEFAULT_ENCODING == "utf-8"
