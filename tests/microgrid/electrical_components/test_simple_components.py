# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for simple leaf electrical components.

These components are plain :class:`ElectricalComponent` subclasses that only fix
their :attr:`category` and add no extra fields. Their behaviour is identical, so
a single parametrized test covers all of them instead of one copy per component.
"""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    Breaker,
    CapacitorBank,
    Chp,
    Converter,
    CryptoMiner,
    ElectricalComponentCategory,
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
    "cls, expected_category",
    [
        (Breaker, ElectricalComponentCategory.BREAKER),
        (CapacitorBank, ElectricalComponentCategory.CAPACITOR_BANK),
        (Chp, ElectricalComponentCategory.CHP),
        (Converter, ElectricalComponentCategory.CONVERTER),
        (CryptoMiner, ElectricalComponentCategory.CRYPTO_MINER),
        (Electrolyzer, ElectricalComponentCategory.ELECTROLYZER),
        (Hvac, ElectricalComponentCategory.HVAC),
        (Meter, ElectricalComponentCategory.METER),
        (Plc, ElectricalComponentCategory.PLC),
        (Precharger, ElectricalComponentCategory.PRECHARGER),
        (StaticTransferSwitch, ElectricalComponentCategory.STATIC_TRANSFER_SWITCH),
        (SteamBoiler, ElectricalComponentCategory.STEAM_BOILER),
        (
            UninterruptiblePowerSupply,
            ElectricalComponentCategory.UNINTERRUPTIBLE_POWER_SUPPLY,
        ),
        (WindTurbine, ElectricalComponentCategory.WIND_TURBINE),
    ],
    ids=lambda value: value.__name__ if isinstance(value, type) else value.name,
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
    expected_category: ElectricalComponentCategory,
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and category of a simple leaf electrical component."""
    component = cls(
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_component",
        _allow_construction=True,
        _provides_telemetry=True,
        _accepts_control=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "test_component"
    assert component.category == expected_category
