# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of inverter types to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import InverterType


def inverter_type_from_proto(
    message: electrical_components_pb2.InverterType.ValueType,
) -> InverterType | int:
    """Convert a protobuf `InverterType` value to a [`InverterType`][....InverterType] enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`InverterType`][....InverterType] enum member, or the
            raw [`int`][] if the protobuf value is not recognized.
    """
    return enum_from_proto(message, InverterType)


def inverter_type_to_proto(
    inverter_type: InverterType,
) -> electrical_components_pb2.InverterType.ValueType:
    """Convert a [`InverterType`][....InverterType] enum member to a protobuf value.

    Args:
        inverter_type: The enum member to convert.

    Returns:
        The corresponding protobuf `InverterType` value.
    """
    return electrical_components_pb2.InverterType.ValueType(inverter_type.value)
