# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for EV charger components."""

import dataclasses

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    AcEvCharger,
    DcEvCharger,
    ElectricalComponentCategory,
    ElectricalComponentId,
    EvCharger,
    EvChargerType,
    HybridEvCharger,
    UnrecognizedEvCharger,
    UnspecifiedEvCharger,
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class EvChargerTestCase:
    """Test case for EV charger components."""

    cls: type[UnspecifiedEvCharger | AcEvCharger | DcEvCharger | HybridEvCharger]
    expected_type: EvChargerType
    name: str


@pytest.fixture
def component_id() -> ElectricalComponentId:
    """Provide a test component ID."""
    return ElectricalComponentId(42)


@pytest.fixture
def microgrid_id() -> MicrogridId:
    """Provide a test microgrid ID."""
    return MicrogridId(1)


def test_abstract_ev_charger_cannot_be_instantiated(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that EvCharger base class cannot be instantiated."""
    with pytest.raises(TypeError, match="Cannot instantiate EvCharger directly"):
        EvCharger(
            id=component_id,
            microgrid_id=microgrid_id,
            name="test_charger",
            _type=1,
            _provides_telemetry=True,
            _accepts_control=True,
        )


@pytest.mark.parametrize(
    "case",
    [
        EvChargerTestCase(
            cls=UnspecifiedEvCharger,
            expected_type=EvChargerType.UNSPECIFIED,
            name="unspecified",
        ),
        EvChargerTestCase(cls=AcEvCharger, expected_type=EvChargerType.AC, name="ac"),
        EvChargerTestCase(cls=DcEvCharger, expected_type=EvChargerType.DC, name="dc"),
        EvChargerTestCase(
            cls=HybridEvCharger,
            expected_type=EvChargerType.HYBRID,
            name="hybrid",
        ),
    ],
    ids=lambda case: case.name,
)
def test_recognized_ev_charger_types(  # Renamed from test_ev_charger_types
    case: EvChargerTestCase,
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and properties of different recognized EV charger types."""
    charger = case.cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name=case.name,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert charger.id == component_id
    assert charger.microgrid_id == microgrid_id
    assert charger.name == case.name
    assert charger.category == ElectricalComponentCategory.EV_CHARGER
    assert charger.type == case.expected_type


def test_unrecognized_ev_charger_type(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of unrecognized EV charger type."""
    charger = UnrecognizedEvCharger(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unrecognized_charger",
        _type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert charger.id == component_id
    assert charger.microgrid_id == microgrid_id
    assert charger.name == "unrecognized_charger"
    assert charger.category == ElectricalComponentCategory.EV_CHARGER
    assert charger.type == 999
