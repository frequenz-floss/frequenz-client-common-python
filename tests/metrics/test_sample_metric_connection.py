# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for MetricConnection and MetricConnectionCategory classes."""

import pytest

from frequenz.client.common.metrics import MetricConnection, MetricConnectionCategory


@pytest.mark.parametrize(
    "category,name,expected_str",
    [
        pytest.param(
            MetricConnectionCategory.BATTERY,
            None,
            "<CATEGORY=BATTERY>",
            id="enum_category_no_name",
        ),
        pytest.param(
            MetricConnectionCategory.PV,
            "dc_pv_0",
            "<CATEGORY=PV>(dc_pv_0)",
            id="enum_category_with_name",
        ),
        pytest.param(
            999,
            None,
            "999",
            id="int_category_no_name",
        ),
        pytest.param(
            999,
            "unknown_connection",
            "999(unknown_connection)",
            id="int_category_with_name",
        ),
    ],
)
def test_str_representation(
    category: MetricConnectionCategory | int,
    name: str | None,
    expected_str: str,
) -> None:
    """Test string representation of MetricConnection."""
    connection = MetricConnection(category=category, name=name)
    assert str(connection) == expected_str


def test_creation_with_enum_category() -> None:
    """Test MetricConnection creation with enum category."""
    connection = MetricConnection(
        category=MetricConnectionCategory.BATTERY,
        name="dc_battery_0",
    )
    assert connection.category == MetricConnectionCategory.BATTERY
    assert connection.name == "dc_battery_0"


def test_creation_with_int_category() -> None:
    """Test MetricConnection creation with int category (unrecognized)."""
    connection = MetricConnection(
        category=999,
        name="unknown",
    )
    assert connection.category == 999
    assert connection.name == "unknown"


def test_creation_default_name() -> None:
    """Test MetricConnection creation with default name."""
    connection = MetricConnection(category=MetricConnectionCategory.AMBIENT)
    assert connection.category == MetricConnectionCategory.AMBIENT
    assert connection.name is None


def test_equality() -> None:
    """Test equality of MetricConnection objects."""
    conn1 = MetricConnection(
        category=MetricConnectionCategory.BATTERY, name="dc_battery_0"
    )
    conn2 = MetricConnection(
        category=MetricConnectionCategory.BATTERY, name="dc_battery_0"
    )
    conn3 = MetricConnection(category=MetricConnectionCategory.PV, name="dc_pv_0")
    assert conn1 == conn2
    assert conn1 != conn3


def test_hash() -> None:
    """Test that MetricConnection objects can be used in sets and as dict keys."""
    conn1 = MetricConnection(
        category=MetricConnectionCategory.BATTERY, name="dc_battery_0"
    )
    conn2 = MetricConnection(
        category=MetricConnectionCategory.BATTERY, name="dc_battery_0"
    )
    conn3 = MetricConnection(category=MetricConnectionCategory.PV, name="dc_pv_0")
    conn_set = {conn1, conn2, conn3}
    assert len(conn_set) == 2  # conn1 and conn2 are equal
