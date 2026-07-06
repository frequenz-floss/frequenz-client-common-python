# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for DeliveryArea and related to/from protobuf v1alpha8 conversion."""

import warnings
from dataclasses import dataclass

import pytest
from frequenz.api.common.v1alpha8.grid import delivery_area_pb2

from frequenz.client.common import UnspecifiedEnumValueError
from frequenz.client.common.grid import EnergyMarketCodeType
from frequenz.client.common.grid.proto.v1alpha8 import (
    delivery_area_from_proto,
    energy_market_code_type_from_proto,
    energy_market_code_type_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestEnergyMarketCodeTypeParity(EnumParityTest):
    """Parity tests for the `EnergyMarketCodeType` enum."""

    python_enum = EnergyMarketCodeType
    proto_enum = delivery_area_pb2.EnergyMarketCodeType
    name_prefix = "ENERGY_MARKET_CODE_TYPE_"
    from_proto = staticmethod(energy_market_code_type_from_proto)
    to_proto = staticmethod(energy_market_code_type_to_proto)
    deprecated_members = frozenset({"UNSPECIFIED"})


@dataclass(frozen=True, kw_only=True)
class _DeliveryAreaProtoConversionTestCase:
    """Test case for protobuf conversion."""

    name: str
    """Description of the test case."""

    code: str | None
    """The code to set in the protobuf message."""

    code_type: int
    """The code type to set in the protobuf message."""

    expected_code: str | None
    """Expected code in the resulting DeliveryArea."""

    expected_code_type: EnergyMarketCodeType | int
    """Expected code type in the resulting DeliveryArea."""

    expect_warning: bool
    """Whether to expect a warning during conversion."""


@pytest.mark.parametrize(
    "case",
    [
        _DeliveryAreaProtoConversionTestCase(
            name="valid_EIC_code",
            code="10Y1001A1001A450",
            code_type=delivery_area_pb2.EnergyMarketCodeType.ENERGY_MARKET_CODE_TYPE_EUROPE_EIC,
            expected_code="10Y1001A1001A450",
            expected_code_type=EnergyMarketCodeType.EUROPE_EIC,
            expect_warning=False,
        ),
        _DeliveryAreaProtoConversionTestCase(
            name="valid_NERC_code",
            code="PJM",
            code_type=delivery_area_pb2.EnergyMarketCodeType.ENERGY_MARKET_CODE_TYPE_US_NERC,
            expected_code="PJM",
            expected_code_type=EnergyMarketCodeType.US_NERC,
            expect_warning=False,
        ),
        _DeliveryAreaProtoConversionTestCase(
            name="no_code",
            code=None,
            code_type=delivery_area_pb2.EnergyMarketCodeType.ENERGY_MARKET_CODE_TYPE_EUROPE_EIC,
            expected_code=None,
            expected_code_type=EnergyMarketCodeType.EUROPE_EIC,
            expect_warning=True,
        ),
        _DeliveryAreaProtoConversionTestCase(
            name="unspecified_code_type",
            code="TEST",
            code_type=delivery_area_pb2.EnergyMarketCodeType.ENERGY_MARKET_CODE_TYPE_UNSPECIFIED,
            expected_code="TEST",
            expected_code_type=0,
            expect_warning=True,
        ),
        _DeliveryAreaProtoConversionTestCase(
            name="unknown_code_type",
            code="TEST",
            code_type=999,
            expected_code="TEST",
            expected_code_type=999,
            expect_warning=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_from_proto(
    caplog: pytest.LogCaptureFixture, case: _DeliveryAreaProtoConversionTestCase
) -> None:
    """Test conversion from protobuf message to DeliveryArea."""
    # We do the type-ignore here because we want to test the case of an
    # arbitrary int too.
    proto = delivery_area_pb2.DeliveryArea(
        code=case.code or "", code_type=case.code_type  # type: ignore[arg-type]
    )
    with caplog.at_level("WARNING"):
        area = delivery_area_from_proto(proto)

    assert area.code == case.expected_code
    assert area.code_type == case.expected_code_type

    if case.expect_warning:
        assert len(caplog.records) > 0
        assert "Found issues in delivery area" in caplog.records[0].message
    else:
        assert len(caplog.records) == 0


def test_get_code_type_from_proto_unspecified_raises() -> None:
    """A proto-loaded unspecified code type raises UnspecifiedEnumValueError."""
    proto = delivery_area_pb2.DeliveryArea(
        code="TEST",
        code_type=(
            delivery_area_pb2.EnergyMarketCodeType.ENERGY_MARKET_CODE_TYPE_UNSPECIFIED
        ),
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        area = delivery_area_from_proto(proto)
    assert area.code_type == 0
    with pytest.raises(UnspecifiedEnumValueError):
        area.get_code_type()
