# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for PowerTransformer component."""

import pytest
from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.components import ComponentId

from frequenz.client.microgrid.component import ComponentCategory, PowerTransformer


@pytest.fixture
def component_id() -> ComponentId:
    """Provide a test component ID."""
    return ComponentId(42)


@pytest.fixture
def microgrid_id() -> MicrogridId:
    """Provide a test microgrid ID."""
    return MicrogridId(1)


@pytest.mark.parametrize(
    "primary, secondary", [(400.0, 230.0), (0.0, 0.0), (230.0, 400.0), (-230.0, -400.0)]
)
def test_creation_ok(
    component_id: ComponentId,
    microgrid_id: MicrogridId,
    primary: float,
    secondary: float,
) -> None:
    """Test PowerTransformer component initialization with different voltages."""
    power_transformer = PowerTransformer(
        id=component_id,
        microgrid_id=microgrid_id,
        name="test_power_transformer",
        manufacturer="test_manufacturer",
        model_name="test_model",
        primary_voltage=primary,
        secondary_voltage=secondary,
    )

    assert power_transformer.id == component_id
    assert power_transformer.microgrid_id == microgrid_id
    assert power_transformer.name == "test_power_transformer"
    assert power_transformer.manufacturer == "test_manufacturer"
    assert power_transformer.model_name == "test_model"
    assert power_transformer.category == ComponentCategory.POWER_TRANSFORMER
    assert power_transformer.primary_voltage == pytest.approx(primary)
    assert power_transformer.secondary_voltage == pytest.approx(secondary)
