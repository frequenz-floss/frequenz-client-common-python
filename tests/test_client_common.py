# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.client.common package."""

from frequenz.client.common.microgrid.components import ComponentCategory


def test_components() -> None:
    """Test the components."""
    for category in ComponentCategory:
        assert ComponentCategory.from_proto(category.to_proto()) == category
