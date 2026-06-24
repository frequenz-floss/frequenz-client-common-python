# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of inverter types to/from protobuf v1alpha8."""

import warnings

import typing_extensions
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import InverterType


@typing_extensions.deprecated(
    "inverter_type_from_proto() is deprecated; use "
    "electrical_component_class_from_proto() instead."
)
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
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return enum_from_proto(message, InverterType)


@typing_extensions.deprecated(
    "inverter_type_to_proto() is deprecated; use "
    "electrical_component_class_to_proto() instead."
)
def inverter_type_to_proto(
    inverter_type: InverterType,
) -> electrical_components_pb2.InverterType.ValueType:
    """Convert a [`InverterType`][....InverterType] enum member to a protobuf value.

    Args:
        inverter_type: The enum member to convert.

    Returns:
        The corresponding protobuf `InverterType` value.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return electrical_components_pb2.InverterType.ValueType(inverter_type.value)
