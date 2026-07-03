# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for Battery components."""

import dataclasses

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    Battery,
    BatteryType,
    ElectricalComponentId,
    LiIonBattery,
    NaIonBattery,
    UnrecognizedBattery,
    UnspecifiedBattery,
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class BatteryTestCase:
    """Test case for battery components."""

    cls: type[UnspecifiedBattery | LiIonBattery | NaIonBattery]
    expected_type: BatteryType
    name: str


@pytest.fixture
def component_id() -> ElectricalComponentId:
    """Provide a test component ID."""
    return ElectricalComponentId(42)


@pytest.fixture
def microgrid_id() -> MicrogridId:
    """Provide a test microgrid ID."""
    return MicrogridId(1)


def test_abstract_battery_cannot_be_instantiated(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that Battery base class cannot be instantiated."""
    with pytest.raises(TypeError, match="Cannot instantiate Battery directly"):
        Battery(
            id=component_id,
            microgrid_id=microgrid_id,
            name="test_battery",
            _type=1,
            _provides_telemetry=True,
            _accepts_control=True,
        )


@pytest.mark.parametrize(
    "case",
    [
        BatteryTestCase(
            cls=UnspecifiedBattery,
            expected_type=BatteryType.UNSPECIFIED,
            name="unspecified",
        ),
        BatteryTestCase(
            cls=LiIonBattery, expected_type=BatteryType.LI_ION, name="li_ion"
        ),
        BatteryTestCase(
            cls=NaIonBattery, expected_type=BatteryType.NA_ION, name="na_ion"
        ),
    ],
    ids=lambda case: case.name,
)
def test_recognized_battery_types(
    case: BatteryTestCase,
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and properties of different battery types."""
    battery = case.cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name=case.name,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert battery.id == component_id
    assert battery.microgrid_id == microgrid_id
    assert battery.name == case.name
    assert battery.type == case.expected_type


def test_unrecognized_battery_type(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of different battery types."""
    battery = UnrecognizedBattery(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unrecognized_battery",
        _type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert battery.id == component_id
    assert battery.microgrid_id == microgrid_id
    assert battery.name == "unrecognized_battery"
    assert battery.type == 999
