# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for MetricConnectionCategory to/from protobuf v1alpha8 conversion.

These tests ensure that, for this version, all enum members are correctly matched by
name and value between the Python `MetricConnectionCategory` enum and the protobuf
`MetricConnectionCategory` enum.
"""

from typing import TypeAlias

import pytest
from frequenz.api.common.v1alpha8.metrics import metrics_pb2

from frequenz.client.common.metrics import MetricConnectionCategory
from frequenz.client.common.metrics.proto.v1alpha8 import (
    metric_connection_category_from_proto,
    metric_connection_category_to_proto,
)

PB_NAMES: list[str] = [
    m.name for m in metrics_pb2.MetricConnectionCategory.DESCRIPTOR.values
]
MetricConnectionCategoryValue: TypeAlias = (
    metrics_pb2.MetricConnectionCategory.ValueType
)

UNKNOWN_PB_VALUE = metrics_pb2.MetricConnectionCategory.ValueType(
    max(m.value for m in MetricConnectionCategory) + 1
)


def test_no_implicit_to_proto_conversion() -> None:
    """Test that protobuf enum values are not implicitly convertible."""
    # mypy should complain about this assignment, so we ignore the type check here.
    # If mypy doesn't find an issue with this conversion, it should complain about
    # the ignore comment having no effect.
    category = list(MetricConnectionCategory)[0]
    _: MetricConnectionCategoryValue = category.value  # type: ignore[assignment]
    metrics_pb2.MetricConnectionCategory.Name(category.value)  # type: ignore[arg-type]


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_proto_enum_matches_enum_name(pb_name: str) -> None:
    """Test that all known protobuf enum names have a matching enum member."""
    pb_value = metrics_pb2.MetricConnectionCategory.Value(pb_name)
    try:
        category = MetricConnectionCategory[
            pb_name.removeprefix("METRIC_CONNECTION_CATEGORY_")
        ]
        assert category.value == pb_value
    except KeyError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_proto_enum_matches_enum_value(pb_name: str) -> None:
    """Test that all known protobuf enum values have a matching enum member."""
    pb_value = metrics_pb2.MetricConnectionCategory.Value(pb_name)
    try:
        category = MetricConnectionCategory(pb_value)
        assert category.value == pb_value
    except ValueError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize(
    "category", list(MetricConnectionCategory), ids=lambda m: m.name
)
def test_enum_matches_proto_enum_name(category: MetricConnectionCategory) -> None:
    """Test that all enum members have a matching protobuf enum name."""
    pb_value = metrics_pb2.MetricConnectionCategory.ValueType(category.value)
    pb_name = metrics_pb2.MetricConnectionCategory.Name(pb_value)
    assert pb_name == f"METRIC_CONNECTION_CATEGORY_{category.name}"


@pytest.mark.parametrize(
    "category", list(MetricConnectionCategory), ids=lambda m: m.name
)
def test_enum_matches_proto_enum_value(category: MetricConnectionCategory) -> None:
    """Test that all enum members have a matching protobuf enum value."""
    pb_value = metrics_pb2.MetricConnectionCategory.Value(
        f"METRIC_CONNECTION_CATEGORY_{category.name}"
    )
    assert category.value == pb_value


@pytest.mark.parametrize("pb_name", PB_NAMES)
def test_from_proto(pb_name: str) -> None:
    """Test conversion from protobuf returns a matching member or int."""
    pb_value = metrics_pb2.MetricConnectionCategory.Value(pb_name)
    category = metric_connection_category_from_proto(pb_value)
    if pb_value in [m.value for m in MetricConnectionCategory]:
        assert category is MetricConnectionCategory(pb_value)
    else:
        assert category == pb_value


def test_from_proto_unknown() -> None:
    """Test conversion from protobuf for yet unknown values return the int."""
    category = metric_connection_category_from_proto(UNKNOWN_PB_VALUE)
    assert isinstance(category, int)
    assert category == UNKNOWN_PB_VALUE


@pytest.mark.parametrize(
    "category", list(MetricConnectionCategory), ids=lambda m: m.name
)
def test_to_proto(category: MetricConnectionCategory) -> None:
    """Test conversion to protobuf return a matching protobuf value."""
    pb_value = metric_connection_category_to_proto(category)
    assert pb_value == category.value
