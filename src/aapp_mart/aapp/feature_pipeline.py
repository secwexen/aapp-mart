"""Deterministic feature preparation pipeline for AAPP."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any


class FeaturePipeline:
    """Validate and prepare feature mappings deterministically."""

    # pylint: disable=too-few-public-methods

    def transform(
        self,
        features: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """Validate and return an immutable, deterministically ordered mapping."""
        normalized_features: dict[str, Any] = {}

        for key in sorted(features):
            if not key.strip():
                raise ValueError("Feature keys must not be empty.")

            normalized_features[key] = features[key]

        return MappingProxyType(normalized_features)


__all__ = ["FeaturePipeline"]
