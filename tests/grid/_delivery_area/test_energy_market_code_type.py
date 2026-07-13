# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the EnergyMarketCodeType enum."""

import pytest

from frequenz.client.common.grid import EnergyMarketCodeType


def test_unspecified_member_is_deprecated() -> None:
    """The UNSPECIFIED member is deprecated; the known members are not."""
    with pytest.deprecated_call():
        deprecated = EnergyMarketCodeType.UNSPECIFIED
    assert deprecated in EnergyMarketCodeType
