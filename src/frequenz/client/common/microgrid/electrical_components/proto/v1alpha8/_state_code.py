# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component state codes to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import ElectricalComponentStateCode


def electrical_component_state_code_from_proto(
    message: electrical_components_pb2.ElectricalComponentStateCode.ValueType,
) -> ElectricalComponentStateCode | int:
    """Convert a protobuf `ElectricalComponentStateCode` value to an enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding
            [`ElectricalComponentStateCode`][....ElectricalComponentStateCode] enum
            member, or the raw [`int`][] if the protobuf value is not recognized.
    """
    return enum_from_proto(message, ElectricalComponentStateCode)


def electrical_component_state_code_to_proto(
    state_code: ElectricalComponentStateCode,
) -> electrical_components_pb2.ElectricalComponentStateCode.ValueType:
    """Convert an `ElectricalComponentStateCode` enum member to a protobuf value.

    Args:
        state_code: The
            [`ElectricalComponentStateCode`][....ElectricalComponentStateCode] enum
            member to convert.

    Returns:
        The corresponding protobuf `ElectricalComponentStateCode` value.
    """
    return electrical_components_pb2.ElectricalComponentStateCode.ValueType(
        state_code.value
    )
