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
    ProblematicElectricalComponent,
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
            model="Test Model",
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
        model="Test Model",
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
        model="Test Model",
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert battery.id == component_id
    assert battery.microgrid_id == microgrid_id
    assert battery.name == "unrecognized_battery"
    assert battery.type == 999


def test_unspecified_battery_is_problematic(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that `UnspecifiedBattery` is a `ProblematicElectricalComponent`."""
    battery = UnspecifiedBattery(
        id=component_id,
        microgrid_id=microgrid_id,
        name="",
        model="Test Model",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert isinstance(battery, ProblematicElectricalComponent)
    assert isinstance(battery, Battery)


def test_unrecognized_battery_is_problematic(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that `UnrecognizedBattery` is a `ProblematicElectricalComponent`."""
    battery = UnrecognizedBattery(
        id=component_id,
        microgrid_id=microgrid_id,
        name="",
        model="Test Model",
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert isinstance(battery, ProblematicElectricalComponent)
    assert isinstance(battery, Battery)


@pytest.mark.parametrize("cls", [LiIonBattery, NaIonBattery])
def test_recognized_battery_types_are_not_problematic(
    cls: type[LiIonBattery | NaIonBattery],
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test that recognized battery types are NOT `ProblematicElectricalComponent`."""
    battery = cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name="",
        model="Test Model",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert not isinstance(battery, ProblematicElectricalComponent)
    assert isinstance(battery, Battery)


def test_unrecognized_battery_str(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """`UnrecognizedBattery.__str__` exposes the raw type after the base label."""
    battery = UnrecognizedBattery(
        id=component_id,
        microgrid_id=microgrid_id,
        name="bat1",
        model="Test Model",
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert str(battery) == "CID42:bat1:Battery:type=999"
