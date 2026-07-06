# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for PowerTransformer component."""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentId,
    PowerTransformer,
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
    "primary, secondary", [(400.0, 230.0), (0.0, 0.0), (230.0, 400.0), (-230.0, -400.0)]
)
def test_creation_ok(
    component_id: ElectricalComponentId,
    microgrid_id: MicrogridId,
    primary: float,
    secondary: float,
) -> None:
    """Test PowerTransformer component initialization with different voltages."""
    power_transformer = PowerTransformer(
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_power_transformer",
        primary_voltage=primary,
        secondary_voltage=secondary,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert power_transformer.id == component_id
    assert power_transformer.microgrid_id == microgrid_id
    assert power_transformer.name == "test_power_transformer"
    assert power_transformer.primary_voltage == pytest.approx(primary)
    assert power_transformer.secondary_voltage == pytest.approx(secondary)
