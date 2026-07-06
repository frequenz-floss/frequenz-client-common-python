# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for Battery components."""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    Battery,
    ElectricalComponentId,
    LiIonBattery,
    NaIonBattery,
    UnrecognizedBattery,
    UnspecifiedBattery,
)


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
            _provides_telemetry=True,
            _accepts_control=True,
        )


@pytest.mark.parametrize(
    "cls",
    [UnspecifiedBattery, LiIonBattery, NaIonBattery],
    ids=lambda cls: cls.__name__,
)
def test_recognized_battery_types(
    cls: type[UnspecifiedBattery | LiIonBattery | NaIonBattery],
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and properties of different battery types."""
    battery = cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_battery",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert battery.id == component_id
    assert battery.microgrid_id == microgrid_id
    assert battery.name == "test_battery"


def test_unrecognized_battery_type(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of different battery types."""
    battery = UnrecognizedBattery(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unrecognized_battery",
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert battery.id == component_id
    assert battery.microgrid_id == microgrid_id
    assert battery.name == "unrecognized_battery"
    assert battery.type == 999
