# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for EV charger components."""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    AcEvCharger,
    DcEvCharger,
    ElectricalComponentId,
    EvCharger,
    HybridEvCharger,
    ProblematicElectricalComponent,
    UnrecognizedEvCharger,
    UnspecifiedEvCharger,
)


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
            _provides_telemetry=True,
            _accepts_control=True,
        )


@pytest.mark.parametrize(
    "cls",
    [UnspecifiedEvCharger, AcEvCharger, DcEvCharger, HybridEvCharger],
    ids=lambda cls: cls.__name__,
)
def test_recognized_ev_charger_types(
    cls: type[UnspecifiedEvCharger | AcEvCharger | DcEvCharger | HybridEvCharger],
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and properties of different recognized EV charger types."""
    charger = cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_charger",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert charger.id == component_id
    assert charger.microgrid_id == microgrid_id
    assert charger.name == "test_charger"


def test_unrecognized_ev_charger_type(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of unrecognized EV charger type."""
    charger = UnrecognizedEvCharger(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unrecognized_charger",
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert charger.id == component_id
    assert charger.microgrid_id == microgrid_id
    assert charger.name == "unrecognized_charger"
    assert charger.type == 999


def test_unspecified_ev_charger_is_problematic(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that `UnspecifiedEvCharger` is a `ProblematicElectricalComponent`."""
    charger = UnspecifiedEvCharger(
        id=component_id,
        microgrid_id=microgrid_id,
        name="",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert isinstance(charger, ProblematicElectricalComponent)
    assert isinstance(charger, EvCharger)


def test_unrecognized_ev_charger_is_problematic(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that `UnrecognizedEvCharger` is a `ProblematicElectricalComponent`."""
    charger = UnrecognizedEvCharger(
        id=component_id,
        microgrid_id=microgrid_id,
        name="",
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert isinstance(charger, ProblematicElectricalComponent)
    assert isinstance(charger, EvCharger)


@pytest.mark.parametrize("cls", [AcEvCharger, DcEvCharger, HybridEvCharger])
def test_recognized_ev_charger_types_are_not_problematic(
    cls: type[AcEvCharger | DcEvCharger | HybridEvCharger],
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test that recognized EV charger types are NOT `ProblematicElectricalComponent`."""
    charger = cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name="",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert not isinstance(charger, ProblematicElectricalComponent)
    assert isinstance(charger, EvCharger)
