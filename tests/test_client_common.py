# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.client.common package."""

from frequenz.client.common.microgrid.components import (
    ComponentCategory,
    ComponentErrorCode,
    ComponentStateCode,
)


def test_components() -> None:
    """Test the components."""
    for category in ComponentCategory:
        assert ComponentCategory.from_proto(category.to_proto()) == category


def test_component_state_code() -> None:
    """Test the component state code."""
    for state_code in ComponentStateCode:
        assert ComponentStateCode.from_proto(state_code.to_proto()) == state_code


def test_component_error_code() -> None:
    """Test the component error code."""
    for error_code in ComponentErrorCode:
        assert ComponentErrorCode.from_proto(error_code.to_proto()) == error_code
