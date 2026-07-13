# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the BaseDeliveryArea class."""

import pytest

from frequenz.client.common.grid import BaseDeliveryArea, EnergyMarketCodeType


def test_cannot_be_instantiated_directly() -> None:
    """`BaseDeliveryArea` refuses direct instantiation."""
    with pytest.raises(TypeError, match="Cannot instantiate BaseDeliveryArea"):
        BaseDeliveryArea(code="TEST", code_type=EnergyMarketCodeType.EUROPE_EIC)
