# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the DeliveryArea class."""

from dataclasses import dataclass

import pytest

from frequenz.client.common.grid import DeliveryArea, EnergyMarketCodeType


@dataclass(frozen=True, kw_only=True)
class _DeliveryAreaTestCase:
    """Test case for DeliveryArea creation."""

    name: str
    """Description of the test case."""

    code: str | None
    """The code to use for the delivery area."""

    code_type: EnergyMarketCodeType | int
    """The type of code being used."""

    expected_str: str
    """Expected string representation."""


@pytest.mark.parametrize(
    "case",
    [
        _DeliveryAreaTestCase(
            name="valid_EIC_code",
            code="10Y1001A1001A450",
            code_type=EnergyMarketCodeType.EUROPE_EIC,
            expected_str="10Y1001A1001A450[EUROPE_EIC]",
        ),
        _DeliveryAreaTestCase(
            name="valid_NERC_code",
            code="PJM",
            code_type=EnergyMarketCodeType.US_NERC,
            expected_str="PJM[US_NERC]",
        ),
        _DeliveryAreaTestCase(
            name="no_code",
            code=None,
            code_type=EnergyMarketCodeType.EUROPE_EIC,
            expected_str="<NO CODE>[EUROPE_EIC]",
        ),
        _DeliveryAreaTestCase(
            name="unspecified_code_type",
            code="TEST",
            code_type=EnergyMarketCodeType.UNSPECIFIED,
            expected_str="TEST[UNSPECIFIED]",
        ),
        _DeliveryAreaTestCase(
            name="unknown_code_type",
            code="TEST",
            code_type=999,
            expected_str="TEST[type=999]",
        ),
    ],
    ids=lambda case: case.name,
)
def test_creation(case: _DeliveryAreaTestCase) -> None:
    """Test creating DeliveryArea instances with various parameters."""
    area = DeliveryArea(code=case.code, code_type=case.code_type)
    assert area.code == case.code
    assert area.code_type == case.code_type
    assert str(area) == case.expected_str


def test_equality() -> None:
    """Test equality of DeliveryArea objects."""
    area1 = DeliveryArea(
        code="10Y1001A1001A450",
        code_type=EnergyMarketCodeType.EUROPE_EIC,
    )
    area2 = DeliveryArea(
        code="10Y1001A1001A450",
        code_type=EnergyMarketCodeType.EUROPE_EIC,
    )
    area3 = DeliveryArea(code="PJM", code_type=EnergyMarketCodeType.US_NERC)

    assert area1 == area2
    assert area1 != area3


def test_hash() -> None:
    """Test that DeliveryArea objects can be used in sets and as dict keys."""
    area1 = DeliveryArea(
        code="10Y1001A1001A450",
        code_type=EnergyMarketCodeType.EUROPE_EIC,
    )
    area2 = DeliveryArea(
        code="10Y1001A1001A450",
        code_type=EnergyMarketCodeType.EUROPE_EIC,
    )
    area3 = DeliveryArea(code="PJM", code_type=EnergyMarketCodeType.US_NERC)

    area_set = {area1, area2, area3}
    assert len(area_set) == 2  # area1 and area2 are equal
