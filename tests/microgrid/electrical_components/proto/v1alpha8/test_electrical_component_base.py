# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for protobuf conversion of the base/common part of electrical components."""

import pytest
from frequenz.api.common.v1alpha8.metrics import bounds_pb2, metrics_pb2
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from google.protobuf.timestamp_pb2 import Timestamp

from frequenz.client.common.metrics import Bounds, Metric
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8._electrical_component import (  # noqa: E501
    _electrical_component_base_from_proto_with_issues,
    _ElectricalComponentBaseData,
    _metric_config_bounds_from_proto,
    _operational_mode_to_bools,
)
from frequenz.client.common.types import Lifetime

from .conftest import base_data_as_proto


@pytest.mark.parametrize(
    "proto_value, expected",
    [
        (
            electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_UNSPECIFIED,
            (None, None),
        ),
        (
            electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_INACTIVE,
            (False, False),
        ),
        (
            electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_TELEMETRY_ONLY,
            (True, False),
        ),
        (
            electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_CONTROL_ONLY,
            (False, True),
        ),
        (
            electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_CONTROL_AND_TELEMETRY,
            (True, True),
        ),
        (999, (None, None)),
    ],
    ids=[
        "unspecified",
        "inactive",
        "telemetry-only",
        "control-only",
        "control-and-telemetry",
        "unknown-int",
    ],
)
def test_operational_mode_to_bools(
    proto_value: int, expected: tuple[bool | None, bool | None]
) -> None:
    """Test that proto operational-mode values map to (provides_telemetry, accepts_control)."""
    assert _operational_mode_to_bools(proto_value) == expected


def test_complete(default_component_base_data: _ElectricalComponentBaseData) -> None:
    """Test parsing of a complete base component proto."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.CHP,  # Just to pick a valid category
    )
    proto = base_data_as_proto(base_data)
    parsed = _electrical_component_base_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert not major_issues
    assert not minor_issues
    assert parsed == base_data


def test_missing_category_specific_info(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """Test parsing with missing optional category specific info."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    base_data = default_component_base_data._replace(
        name=None,
        category=ElectricalComponentCategory.UNSPECIFIED,
        lifetime=Lifetime(),
        metric_config_bounds={},
        category_specific_info={},
    )
    proto = base_data_as_proto(base_data)
    proto.ClearField("operational_lifetime")
    proto.ClearField("metric_config_bounds")

    parsed = _electrical_component_base_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert sorted(major_issues) == sorted(["category is unspecified"])
    assert sorted(minor_issues) == sorted(
        [
            "name is empty",
            "missing operational lifetime, considering it always operational",
        ]
    )
    assert parsed == base_data


def test_category_specific_info_mismatch(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """Test category and category specific info mismatch."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.GRID_CONNECTION_POINT,
        category_specific_info={"type": "BATTERY_TYPE_LI_ION"},
        category_mismatched=True,
    )
    proto = base_data_as_proto(base_data)
    proto.category_specific_info.battery.type = (
        electrical_components_pb2.BATTERY_TYPE_LI_ION
    )

    parsed = _electrical_component_base_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )
    # Actual message from _electrical_component_base_from_proto_with_issues
    assert major_issues == [
        "category_specific_info.kind (battery) does not match the category (grid_connection_point)"
    ]
    assert not minor_issues
    assert parsed == base_data


def test_invalid_lifetime(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """Test invalid lifetime (start after end)."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.CHP, lifetime=Lifetime()
    )
    proto = base_data_as_proto(base_data)
    proto.operational_lifetime.start_timestamp.CopyFrom(
        Timestamp(seconds=1696204800)  # 2023-10-02T00:00:00Z
    )
    proto.operational_lifetime.end_timestamp.CopyFrom(
        Timestamp(seconds=1696118400)  # 2023-10-01T00:00:00Z
    )

    parsed = _electrical_component_base_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert major_issues == [
        "invalid operational lifetime (Start (2023-10-02 00:00:00+00:00) must be "
        "before or equal to end (2023-10-01 00:00:00+00:00)), considering it as "
        "missing (i.e. always operational)"
    ]
    assert not minor_issues
    assert parsed == base_data


_UNKNOWN_METRIC_INT = 9999
"""A metric int with no corresponding `Metric` member (forward-compat case)."""


def _metric_bound(
    metric_value: int, lower: float, upper: float
) -> electrical_components_pb2.MetricConfigBounds:
    """Build a `MetricConfigBounds` proto for the given raw metric int and bounds."""
    return electrical_components_pb2.MetricConfigBounds(
        metric=metrics_pb2.Metric.ValueType(metric_value),
        config_bounds=bounds_pb2.Bounds(lower=lower, upper=upper),
    )


def test_metric_config_bounds_drops_unspecified() -> None:
    """Test UNSPECIFIED keys drop on load while unknown-int and real metrics survive."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    message = [
        _metric_bound(int(Metric.UNSPECIFIED.value), 0.0, 1.0),
        _metric_bound(_UNKNOWN_METRIC_INT, 2.0, 3.0),
        _metric_bound(int(Metric.DC_VOLTAGE.value), 4.0, 5.0),
    ]

    parsed = _metric_config_bounds_from_proto(
        message, major_issues=major_issues, minor_issues=minor_issues
    )

    assert Metric.UNSPECIFIED not in parsed
    assert parsed[_UNKNOWN_METRIC_INT] == Bounds(lower=2.0, upper=3.0)
    assert parsed[Metric.DC_VOLTAGE] == Bounds(lower=4.0, upper=5.0)
    assert any(
        "UNSPECIFIED" in issue and "drop" in issue.lower() for issue in major_issues
    )
    assert any(str(_UNKNOWN_METRIC_INT) in issue for issue in minor_issues)
