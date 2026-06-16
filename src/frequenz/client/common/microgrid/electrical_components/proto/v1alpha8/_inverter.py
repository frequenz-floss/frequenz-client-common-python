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
    """Convert a protobuf InverterType enum value to an enum member.

    Args:
        message: A protobuf InverterType enum value.

    Returns:
        The corresponding InverterType enum member, or the raw `int` if the
            protobuf value is not recognized.
    """
    return enum_from_proto(message, InverterType)


def inverter_type_to_proto(
    inverter_type: InverterType,
) -> electrical_components_pb2.InverterType.ValueType:
    """Convert an InverterType enum member to a protobuf enum value.

    Args:
        inverter_type: An InverterType enum member.

    Returns:
        The corresponding protobuf InverterType enum value.
    """
    return electrical_components_pb2.InverterType.ValueType(inverter_type.value)
