# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of battery types to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import BatteryType


def battery_type_from_proto(
    message: electrical_components_pb2.BatteryType.ValueType,
) -> BatteryType | int:
    """Convert a protobuf `BatteryType` value to a [`BatteryType`][....BatteryType] enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`BatteryType`][....BatteryType] enum member, or the raw
            [`int`][] if the protobuf value is not recognized.
    """
    return enum_from_proto(message, BatteryType)


def battery_type_to_proto(
    battery_type: BatteryType,
) -> electrical_components_pb2.BatteryType.ValueType:
    """Convert a [`BatteryType`][....BatteryType] enum member to a protobuf value.

    Args:
        battery_type: The enum member to convert.

    Returns:
        The corresponding protobuf `BatteryType` value.
    """
    return electrical_components_pb2.BatteryType.ValueType(battery_type.value)
