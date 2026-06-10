# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Tests for the deprecated metric module."""

import pytest

from frequenz.client.common.metric import Metric


def test_metric_class_deprecated() -> None:
    """Test that using the deprecated Metric enum emits a deprecation warning."""
    with pytest.deprecated_call():
        assert Metric(Metric.UNSPECIFIED.value) is Metric.UNSPECIFIED
