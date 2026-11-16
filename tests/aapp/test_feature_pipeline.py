"""Tests for the AAPP feature preparation pipeline."""

from collections.abc import MutableMapping
from typing import Any, cast

import pytest

from aapp_mart.aapp.feature_pipeline import FeaturePipeline

# pylint: disable=redefined-outer-name


@pytest.fixture
def feature_pipeline() -> FeaturePipeline:
    """Provide a feature pipeline instance."""
    return FeaturePipeline()


def test_transform_returns_feature_mapping(
    feature_pipeline: FeaturePipeline,
) -> None:
    """Return the supplied feature data."""
    features: dict[str, Any] = {
        "hostname": "server-01",
        "port": 443,
        "is_external": True,
    }

    result = feature_pipeline.transform(features)

    assert dict(result) == features


def test_transform_sorts_feature_keys(
    feature_pipeline: FeaturePipeline,
) -> None:
    """Return feature keys in deterministic sorted order."""
    features: dict[str, Any] = {
        "zeta": 3,
        "alpha": 1,
        "gamma": 2,
    }

    result = feature_pipeline.transform(features)

    assert list(result.keys()) == ["alpha", "gamma", "zeta"]


def test_transform_returns_immutable_mapping(
    feature_pipeline: FeaturePipeline,
) -> None:
    """Prevent modification of the returned feature mapping."""
    features: dict[str, Any] = {
        "hostname": "server-01",
    }

    result = feature_pipeline.transform(features)

    mutable_result = cast(
        MutableMapping[str, Any],
        result,
    )

    with pytest.raises(TypeError):
        mutable_result["hostname"] = "server-02"


def test_transform_does_not_modify_input(
    feature_pipeline: FeaturePipeline,
) -> None:
    """Preserve the original input mapping."""
    features: dict[str, Any] = {
        "zeta": 3,
        "alpha": 1,
    }
    original = features.copy()

    feature_pipeline.transform(features)

    assert features == original


def test_transform_rejects_empty_feature_key(
    feature_pipeline: FeaturePipeline,
) -> None:
    """Reject empty feature names."""
    features: dict[str, Any] = {
        "": "invalid",
    }

    with pytest.raises(
        ValueError,
        match="Feature keys must not be empty",
    ):
        feature_pipeline.transform(features)


def test_transform_rejects_whitespace_feature_key(
    feature_pipeline: FeaturePipeline,
) -> None:
    """Reject feature names containing only whitespace."""
    features: dict[str, Any] = {
        "   ": "invalid",
    }

    with pytest.raises(
        ValueError,
        match="Feature keys must not be empty",
    ):
        feature_pipeline.transform(features)


def test_transform_supports_empty_mapping(
    feature_pipeline: FeaturePipeline,
) -> None:
    """Accept an empty feature mapping."""
    result = feature_pipeline.transform({})

    assert not result
