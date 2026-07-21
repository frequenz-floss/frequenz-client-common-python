# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for protobuf conversion of the base/common part of electrical components."""

from datetime import timezone

import pytest
from frequenz.api.common.v1alpha8.metrics import bounds_pb2, metrics_pb2
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from google.protobuf.timestamp_pb2 import Timestamp

from frequenz.client.common.metrics import Bounds, InvalidBounds, Metric
from frequenz.client.common.microgrid import InvalidLifetime, Lifetime
from frequenz.client.common.microgrid.electrical_components import (
    CategorySpecificInfo,
    ElectricalComponentCategory,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8._electrical_component import (  # noqa: E501
    _electrical_component_base_from_proto_with_issues,
    _ElectricalComponentBaseData,
    _metric_config_bounds_from_proto,
    _operational_mode_to_bools,
)

from .conftest import base_data_as_proto


@pytest.mark.parametrize(
    "proto_value, expected",
    [
        (
            electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_UNSPECIFIED,
            (0, 0),
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
        (999, (999, 999)),
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
    proto_value: int, expected: tuple[bool | int, bool | int]
) -> None:
    """Test that proto operational-mode values map to (provides_telemetry, accepts_control)."""
    result = _operational_mode_to_bools(proto_value)
    assert result == expected
    # The raw int representation must be preserved as `int` (not `bool`) so the
    # higher-level accessor can distinguish unspecified (0) from unrecognized
    # values and from recognized False (which compares equal to 0).
    assert type(result[0]) is type(expected[0])
    assert type(result[1]) is type(expected[1])


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
        name="",
        category=ElectricalComponentCategory.UNSPECIFIED,
        lifetime=Lifetime(),
        metric_config_bounds={},
        category_specific_info=None,
    )
    proto = base_data_as_proto(base_data)
    proto.ClearField("operational_lifetime")
    proto.ClearField("metric_config_bounds")

    parsed = _electrical_component_base_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert sorted(major_issues) == sorted(["category is unspecified"])
    assert not minor_issues
    assert parsed == base_data


def test_empty_lifetime_is_unbounded(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """A present but empty protobuf lifetime becomes an unbounded `Lifetime`."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.CHP,
        lifetime=Lifetime(),
    )
    proto = base_data_as_proto(base_data)

    assert proto.HasField("operational_lifetime")
    parsed = _electrical_component_base_from_proto_with_issues(
        proto, major_issues=major_issues, minor_issues=minor_issues
    )

    assert not major_issues
    assert not minor_issues
    assert parsed == base_data


def test_category_specific_info_mismatch(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """Test category and category specific info mismatch."""
    major_issues: list[str] = []
    minor_issues: list[str] = []
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.GRID_CONNECTION_POINT,
        category_specific_info=CategorySpecificInfo(
            kind="battery", fields={"type": "BATTERY_TYPE_LI_ION"}
        ),
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
        category=ElectricalComponentCategory.CHP,
        lifetime=InvalidLifetime(
            start_time=Timestamp(seconds=1696204800).ToDatetime(tzinfo=timezone.utc),
            end_time=Timestamp(seconds=1696118400).ToDatetime(tzinfo=timezone.utc),
        ),
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

    assert not major_issues
    assert not minor_issues
    assert parsed == base_data


_UNKNOWN_METRIC_INT = 9999
"""A metric int with no corresponding `Metric` member (forward-compat case)."""


def _metric_bound(
    metric_value: int, lower: float | int, upper: float | int
) -> electrical_components_pb2.MetricConfigBounds:
    """Build a `MetricConfigBounds` proto for the given raw metric int and bounds."""
    return electrical_components_pb2.MetricConfigBounds(
        metric=metrics_pb2.Metric.ValueType(metric_value),
        config_bounds=bounds_pb2.Bounds(lower=lower, upper=upper),
    )


def test_metric_config_bounds_stores_unspecified_as_int() -> None:
    """Test UNSPECIFIED metric bounds load as plain int key 0."""
    message = [
        _metric_bound(int(Metric.UNSPECIFIED.value), 0.0, 1.0),
        _metric_bound(_UNKNOWN_METRIC_INT, 2.0, 3.0),
        _metric_bound(int(Metric.DC_VOLTAGE.value), 4.0, 5.0),
    ]

    parsed = _metric_config_bounds_from_proto(message)

    assert parsed[int(Metric.UNSPECIFIED.value)] == Bounds(lower=0.0, upper=1.0)
    assert Metric.UNSPECIFIED not in parsed
    assert parsed[_UNKNOWN_METRIC_INT] == Bounds(lower=2.0, upper=3.0)
    assert parsed[Metric.DC_VOLTAGE] == Bounds(lower=4.0, upper=5.0)


def test_metric_config_bounds_preserves_invalid_bounds() -> None:
    """Invalid bounds are preserved as `InvalidBounds` entries, not skipped."""
    message = [
        _metric_bound(int(Metric.DC_VOLTAGE.value), 10.0, -10.0),
        _metric_bound(int(Metric.AC_POWER_ACTIVE.value), -5.0, 5.0),
    ]

    parsed = _metric_config_bounds_from_proto(message)

    invalid = parsed[Metric.DC_VOLTAGE]
    assert isinstance(invalid, InvalidBounds)
    assert not isinstance(invalid, Bounds)
    assert invalid.lower == 10.0
    assert invalid.upper == -10.0
    assert parsed[Metric.AC_POWER_ACTIVE] == Bounds(lower=-5.0, upper=5.0)


def test_metric_config_bounds_absent_config_bounds_is_unbounded() -> None:
    """An entry without a `config_bounds` field yields an unbounded `Bounds`."""
    entry = electrical_components_pb2.MetricConfigBounds(
        metric=metrics_pb2.Metric.ValueType(int(Metric.DC_VOLTAGE.value))
    )
    entry.ClearField("config_bounds")

    parsed = _metric_config_bounds_from_proto([entry])

    assert parsed[Metric.DC_VOLTAGE] == Bounds()


def test_metric_config_bounds_duplicated_metric_last_wins() -> None:
    """A duplicated metric on the wire is kept as its last entry (proto3 map semantics)."""
    message = [
        _metric_bound(int(Metric.DC_VOLTAGE.value), 0.0, 1.0),
        _metric_bound(int(Metric.DC_VOLTAGE.value), 2.0, 3.0),
    ]

    parsed = _metric_config_bounds_from_proto(message)

    assert parsed[Metric.DC_VOLTAGE] == Bounds(lower=2.0, upper=3.0)
