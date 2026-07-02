# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of EV charger types to/from protobuf v1alpha8."""

import warnings

import typing_extensions
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import EvChargerType


@typing_extensions.deprecated(
    "ev_charger_type_from_proto() is deprecated; use "
    "electrical_component_class_from_proto() instead."
)
def ev_charger_type_from_proto(
    message: electrical_components_pb2.EvChargerType.ValueType,
) -> EvChargerType | int:
    """Convert a protobuf `EvChargerType` value to an enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`EvChargerType`][....EvChargerType] enum member, or the
            raw [`int`][] if the protobuf value is not recognized.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return enum_from_proto(message, EvChargerType)


@typing_extensions.deprecated(
    "ev_charger_type_to_proto() is deprecated; use "
    "electrical_component_class_to_proto() instead."
)
def ev_charger_type_to_proto(
    ev_charger_type: EvChargerType,
) -> electrical_components_pb2.EvChargerType.ValueType:
    """Convert a [`EvChargerType`][....EvChargerType] enum member to a protobuf value.

    Args:
        ev_charger_type: The enum member to convert.

    Returns:
        The corresponding protobuf `EvChargerType` value.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return electrical_components_pb2.EvChargerType.ValueType(ev_charger_type.value)
