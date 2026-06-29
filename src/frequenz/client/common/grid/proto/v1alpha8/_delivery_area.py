# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Conversion of DeliveryArea and EnergyMarketCodeType to/from protobuf v1alpha8."""

import logging

from frequenz.api.common.v1alpha8.grid import delivery_area_pb2

from ....proto import enum_from_proto
from ..._delivery_area import DeliveryArea, EnergyMarketCodeType

_logger = logging.getLogger(__name__)


def energy_market_code_type_from_proto(
    message: delivery_area_pb2.EnergyMarketCodeType.ValueType,
) -> EnergyMarketCodeType | int:
    """Convert a protobuf `EnergyMarketCodeType` value to an enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding EnergyMarketCodeType enum member, or the raw `int` if the
            protobuf value is not recognized.
    """
    return enum_from_proto(message, EnergyMarketCodeType)


def energy_market_code_type_to_proto(
    code_type: EnergyMarketCodeType,
) -> delivery_area_pb2.EnergyMarketCodeType.ValueType:
    """Convert an EnergyMarketCodeType enum member to a protobuf enum value.

    Args:
        code_type: The enum member to convert.

    Returns:
        The corresponding protobuf `EnergyMarketCodeType` value.
    """
    return delivery_area_pb2.EnergyMarketCodeType.ValueType(code_type.value)


def delivery_area_from_proto(message: delivery_area_pb2.DeliveryArea) -> DeliveryArea:
    """Convert a protobuf delivery area message to a delivery area object.

    Args:
        message: The protobuf message to convert.

    Returns:
        The resulting delivery area object.
    """
    issues: list[str] = []

    code = message.code or None
    if code is None:
        issues.append("code is empty")

    code_type = energy_market_code_type_from_proto(message.code_type)
    if code_type is EnergyMarketCodeType.UNSPECIFIED:
        issues.append("code_type is unspecified")
    elif isinstance(code_type, int):
        issues.append("code_type is unrecognized")

    if issues:
        _logger.warning(
            "Found issues in delivery area: %s | Protobuf message:\n%s",
            ", ".join(issues),
            message,
        )

    return DeliveryArea(code=code, code_type=code_type)
