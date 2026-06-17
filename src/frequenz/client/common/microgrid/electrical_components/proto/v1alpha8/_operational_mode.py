# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component operational modes to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import ElectricalComponentOperationalMode


def electrical_component_operational_mode_from_proto(
    message: electrical_components_pb2.ElectricalComponentOperationalMode.ValueType,
) -> ElectricalComponentOperationalMode | int:
    """Convert a protobuf ElectricalComponentOperationalMode enum value to an enum member.

    Args:
        message: A protobuf ElectricalComponentOperationalMode enum value.

    Returns:
        The corresponding ElectricalComponentOperationalMode enum member, or the raw
            `int` if the protobuf value is not recognized.
    """
    return enum_from_proto(message, ElectricalComponentOperationalMode)


def electrical_component_operational_mode_to_proto(
    operational_mode: ElectricalComponentOperationalMode,
) -> electrical_components_pb2.ElectricalComponentOperationalMode.ValueType:
    """Convert an ElectricalComponentOperationalMode enum member to a protobuf enum value.

    Args:
        operational_mode: An ElectricalComponentOperationalMode enum member.

    Returns:
        The corresponding protobuf ElectricalComponentOperationalMode enum value.
    """
    return electrical_components_pb2.ElectricalComponentOperationalMode.ValueType(
        operational_mode.value
    )
