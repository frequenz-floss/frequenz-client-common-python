# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for problematic electrical components."""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    CategorySpecificInfo,
    ElectricalComponentId,
    MismatchedCategoryElectricalComponent,
    ProblematicElectricalComponent,
    UnrecognizedElectricalComponent,
    UnspecifiedElectricalComponent,
)


@pytest.fixture
def component_id() -> ElectricalComponentId:
    """Provide a test electrical component ID."""
    return ElectricalComponentId(42)


@pytest.fixture
def microgrid_id() -> MicrogridId:
    """Provide a test microgrid ID."""
    return MicrogridId(1)


def test_abstract_problematic_electrical_component_cannot_be_instantiated(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test that ProblematicElectricalComponent cannot be instantiated."""
    with pytest.raises(
        TypeError, match="Cannot instantiate ProblematicElectricalComponent directly"
    ):
        ProblematicElectricalComponent(
            id=component_id,
            microgrid_id=microgrid_id,
            name="test_problematic",
            model="Test Model",
            _provides_telemetry=True,
            _accepts_control=True,
        )


def test_unspecified_component(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of UnspecifiedElectricalComponent."""
    component = UnspecifiedElectricalComponent(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unspecified_component",
        model="Test Model",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "unspecified_component"


def test_mismatched_category_component_with_known_category(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test MismatchedCategoryElectricalComponent with a known category."""
    expected_category = 5  # Battery
    component = MismatchedCategoryElectricalComponent(
        id=component_id,
        microgrid_id=microgrid_id,
        name="mismatched_battery",
        model="Test Model",
        category=expected_category,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "mismatched_battery"
    assert component.category == expected_category


def test_mismatched_category_component_with_unrecognized_category(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test MismatchedCategoryElectricalComponent with an unrecognized category."""
    expected_category = 999
    component = MismatchedCategoryElectricalComponent(
        id=component_id,
        microgrid_id=microgrid_id,
        name="mismatched_unrecognized",
        model="Test Model",
        category=expected_category,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "mismatched_unrecognized"
    assert component.category == expected_category


def test_unrecognized_component_type(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test initialization and properties of UnrecognizedElectricalComponent."""
    component = UnrecognizedElectricalComponent(
        id=component_id,
        microgrid_id=microgrid_id,
        name="unrecognized_component",
        model="Test Model",
        category=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "unrecognized_component"
    assert component.category == 999


def test_unrecognized_component_str(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """`UnrecognizedElectricalComponent.__str__` exposes the raw category."""
    component = UnrecognizedElectricalComponent(
        id=component_id,
        microgrid_id=microgrid_id,
        name="comp1",
        model="Test Model",
        category=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert str(component) == "CID42:comp1:category=999"


def test_mismatched_category_component_str(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """`MismatchedCategoryElectricalComponent.__str__` exposes the mismatch."""
    component = MismatchedCategoryElectricalComponent(
        id=component_id,
        microgrid_id=microgrid_id,
        name="comp1",
        model="Test Model",
        category=5,  # BATTERY
        category_name="BATTERY",
        category_specific_info=CategorySpecificInfo(kind="inverter", fields={}),
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert str(component) == "CID42:comp1:mismatched:category=BATTERY:kind=inverter"
