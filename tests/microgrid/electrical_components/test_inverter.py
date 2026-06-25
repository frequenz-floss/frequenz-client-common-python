# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for Inverter components."""

import dataclasses

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    BatteryInverter,
    ElectricalComponentCategory,
    ElectricalComponentId,
    HybridInverter,
    Inverter,
    InverterType,
    PvInverter,
    UnrecognizedInverter,
    UnspecifiedInverter,
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class InverterTestCase:
    """Test case for Inverter components."""

    cls: type[UnspecifiedInverter | BatteryInverter | PvInverter | HybridInverter]
    expected_type: InverterType
    name: str


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
            _type=1,
            _provides_telemetry=True,
            _accepts_control=True,
        )


@pytest.mark.parametrize(
    "case",
    [
        InverterTestCase(
            cls=UnspecifiedInverter,
            expected_type=InverterType.UNSPECIFIED,
            name="unspecified",
        ),
        InverterTestCase(
            cls=BatteryInverter, expected_type=InverterType.BATTERY, name="battery"
        ),
        InverterTestCase(cls=PvInverter, expected_type=InverterType.PV, name="pv"),
        InverterTestCase(
            cls=HybridInverter, expected_type=InverterType.HYBRID, name="hybrid"
        ),
    ],
    ids=lambda case: case.name,
)
def test_recognized_inverter_types(
    case: InverterTestCase,
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and properties of different recognized inverter types."""
    inverter = case.cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name=case.name,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert inverter.id == component_id
    assert inverter.microgrid_id == microgrid_id
    assert inverter.name == case.name
    assert inverter.category == ElectricalComponentCategory.INVERTER
    assert inverter.type == case.expected_type


def test_unrecognized_inverter_type(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of unrecognized inverter type."""
    inverter = UnrecognizedInverter(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unrecognized_inverter",
        _type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert inverter.id == component_id
    assert inverter.microgrid_id == microgrid_id
    assert inverter.name == "unrecognized_inverter"
    assert inverter.category == ElectricalComponentCategory.INVERTER
    assert inverter.type == 999
