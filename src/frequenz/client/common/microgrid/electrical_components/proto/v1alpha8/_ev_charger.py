# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of EV charger types to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import EvChargerType


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
    return enum_from_proto(message, EvChargerType)


def ev_charger_type_to_proto(
    ev_charger_type: EvChargerType,
) -> electrical_components_pb2.EvChargerType.ValueType:
    """Convert a [`EvChargerType`][....EvChargerType] enum member to a protobuf value.

    Args:
        ev_charger_type: The enum member to convert.

    Returns:
        The corresponding protobuf `EvChargerType` value.
    """
    return electrical_components_pb2.EvChargerType.ValueType(ev_charger_type.value)
