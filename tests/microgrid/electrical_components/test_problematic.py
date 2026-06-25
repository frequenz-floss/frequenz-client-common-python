# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for problematic electrical components."""

import pytest

from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
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
            _category=0,
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
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "unspecified_component"
    assert component.category == ElectricalComponentCategory.UNSPECIFIED


def test_mismatched_category_component_with_known_category(
    component_id: ElectricalComponentId, microgrid_id: MicrogridId
) -> None:
    """Test MismatchedCategoryElectricalComponent with a known category."""
    expected_category = 5  # Battery
    component = MismatchedCategoryElectricalComponent(
        id=component_id,
        microgrid_id=microgrid_id,
        name="mismatched_battery",
        _category=expected_category,
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
        _category=expected_category,
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
        _category=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.id == component_id
    assert component.microgrid_id == microgrid_id
    assert component.name == "unrecognized_component"
    assert component.category == 999
