# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.client.common package."""

from frequenz.client.common.v1alpha8.microgrid.electrical_components import (
    ElectricalComponentCategory,
    ElectricalComponentDiagnosticCode,
    ElectricalComponentStateCode,
)


def test_components() -> None:
    """Test the components."""
    for category in ElectricalComponentCategory:
        assert ElectricalComponentCategory.from_proto(category.to_proto()) == category


def test_component_state_code() -> None:
    """Test the component state code."""
    for state_code in ElectricalComponentStateCode:
        assert (
            ElectricalComponentStateCode.from_proto(state_code.to_proto()) == state_code
        )


def test_component_error_code() -> None:
    """Test the component diagnostic code."""
    for diagnostic_code in ElectricalComponentDiagnosticCode:
        assert (
            ElectricalComponentDiagnosticCode.from_proto(diagnostic_code.to_proto())
            == diagnostic_code
        )
