# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of battery types to/from protobuf v1alpha8."""

import warnings

import typing_extensions
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import BatteryType


@typing_extensions.deprecated(
    "battery_type_from_proto() is deprecated; use "
    "electrical_component_class_from_proto() instead."
)
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
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return enum_from_proto(message, BatteryType)


@typing_extensions.deprecated(
    "battery_type_to_proto() is deprecated; use "
    "electrical_component_class_to_proto() instead."
)
def battery_type_to_proto(
    battery_type: BatteryType,
) -> electrical_components_pb2.BatteryType.ValueType:
    """Convert a [`BatteryType`][....BatteryType] enum member to a protobuf value.

    Args:
        battery_type: The enum member to convert.

    Returns:
        The corresponding protobuf `BatteryType` value.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return electrical_components_pb2.BatteryType.ValueType(battery_type.value)
