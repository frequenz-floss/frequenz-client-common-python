# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for Inverter components."""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    BatteryInverter,
    ElectricalComponentId,
    HybridInverter,
    Inverter,
    PvInverter,
    UnrecognizedInverter,
    UnspecifiedInverter,
)


@pytest.fixture
def component_id() -> ElectricalComponentId:
    """Provide a test component ID."""
    return ElectricalComponentId(42)


@pytest.fixture
def microgrid_id() -> MicrogridId:
    """Provide a test microgrid ID."""
    return MicrogridId(1)


def test_abstract_inverter_cannot_be_instantiated(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that Inverter base class cannot be instantiated."""
    with pytest.raises(TypeError, match="Cannot instantiate Inverter directly"):
        Inverter(
            id=component_id,
            microgrid_id=microgrid_id,
            name="test_inverter",
            _provides_telemetry=True,
            _accepts_control=True,
        )


@pytest.mark.parametrize(
    "cls",
    [UnspecifiedInverter, BatteryInverter, PvInverter, HybridInverter],
    ids=lambda cls: cls.__name__,
)
def test_recognized_inverter_types(
    cls: type[UnspecifiedInverter | BatteryInverter | PvInverter | HybridInverter],
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and properties of different recognized inverter types."""
    inverter = cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_inverter",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert inverter.id == component_id
    assert inverter.microgrid_id == microgrid_id
    assert inverter.name == "test_inverter"


def test_unrecognized_inverter_type(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of unrecognized inverter type."""
    inverter = UnrecognizedInverter(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unrecognized_inverter",
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert inverter.id == component_id
    assert inverter.microgrid_id == microgrid_id
    assert inverter.name == "unrecognized_inverter"
    assert inverter.type == 999
