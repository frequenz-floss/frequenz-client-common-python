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
    Chp,
    Converter,
    CryptoMiner,
    ElectricalComponent,
    ElectricalComponentCategory,
    ElectricalComponentId,
    Electrolyzer,
    Hvac,
    Meter,
    Precharger,
    Relay,
    SteamBoiler,
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
        (Chp, ElectricalComponentCategory.CHP),
        (Converter, ElectricalComponentCategory.CONVERTER),
        (CryptoMiner, ElectricalComponentCategory.CRYPTO_MINER),
        (Electrolyzer, ElectricalComponentCategory.ELECTROLYZER),
        (Hvac, ElectricalComponentCategory.HVAC),
        (Meter, ElectricalComponentCategory.METER),
        (Precharger, ElectricalComponentCategory.PRECHARGER),
        (Relay, ElectricalComponentCategory.BREAKER),
        (SteamBoiler, ElectricalComponentCategory.STEAM_BOILER),
        (WindTurbine, ElectricalComponentCategory.WIND_TURBINE),
    ],
    ids=lambda value: value.__name__ if isinstance(value, type) else value.name,
)
def test_init(
    cls: type[ElectricalComponent],
    expected_category: ElectricalComponentCategory,
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
) -> None:
    """Test initialization and category of a simple leaf electrical component."""
    # We need to ignore call-arg because otherwise mypy complains about a missing
    # category argument. It seems by doing this `cls` trick, mypy can't figure out
    # the concrete class we are instantiating has a default category specified, so
    # we don't really need to specify the category explicitly.
    component = cls(  # type: ignore[call-arg]
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_component",
        manufacturer="test_manufacturer",
        model_name="test_model",
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "test_component"
    assert component.manufacturer == "test_manufacturer"
    assert component.model_name == "test_model"
    assert component.category == expected_category
