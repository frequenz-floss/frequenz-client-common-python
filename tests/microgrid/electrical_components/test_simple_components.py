# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for simple leaf electrical components.

These components are plain :class:`ElectricalComponent` subclasses that add no
extra fields. Their behaviour is identical, so a single parametrized test
covers all of them instead of one copy per component.
"""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    Breaker,
    CapacitorBank,
    Chp,
    Converter,
    CryptoMiner,
    ElectricalComponentId,
    Electrolyzer,
    Hvac,
    Meter,
    Plc,
    Precharger,
    StaticTransferSwitch,
    SteamBoiler,
    UninterruptiblePowerSupply,
    WindTurbine,
)


@pytest.fixture
def component_id() -> ElectricalComponentId:
    """Provide a test component ID."""
    return ElectricalComponentId(42)


@pytest.fixture
def microgrid_id() -> MicrogridId:
    """Provide a test microgrid ID."""
    return MicrogridId(1)


@pytest.mark.parametrize(
    "cls",
    [
        Breaker,
        CapacitorBank,
        Chp,
        Converter,
        CryptoMiner,
        Electrolyzer,
        Hvac,
        Meter,
        Plc,
        Precharger,
        StaticTransferSwitch,
        SteamBoiler,
        UninterruptiblePowerSupply,
        WindTurbine,
    ],
    ids=lambda cls: cls.__name__,
)
def test_init(
    cls: type[
        Breaker
        | CapacitorBank
        | Chp
        | Converter
        | CryptoMiner
        | Electrolyzer
        | Hvac
        | Meter
        | Plc
        | Precharger
        | StaticTransferSwitch
        | SteamBoiler
        | UninterruptiblePowerSupply
        | WindTurbine
    ],
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization of a simple leaf electrical component."""
    component = cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_component",
        model="Test Model",
        _allow_construction=True,
        _provides_telemetry=True,
        _accepts_control=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "test_component"
