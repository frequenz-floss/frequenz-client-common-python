# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component categories to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import ElectricalComponentCategory


def electrical_component_category_from_proto(
    message: electrical_components_pb2.ElectricalComponentCategory.ValueType,
) -> ElectricalComponentCategory | int:
    """Convert a protobuf ElectricalComponentCategory enum value to an enum member.

    Args:
        message: A protobuf ElectricalComponentCategory enum value.

    Returns:
        The corresponding ElectricalComponentCategory enum member, or the raw `int`
            if the protobuf value is not recognized.
    """
    return enum_from_proto(message, ElectricalComponentCategory)


def electrical_component_category_to_proto(
    category: ElectricalComponentCategory,
) -> electrical_components_pb2.ElectricalComponentCategory.ValueType:
    """Convert an ElectricalComponentCategory enum member to a protobuf enum value.

    Args:
        category: An ElectricalComponentCategory enum member.

    Returns:
        The corresponding protobuf ElectricalComponentCategory enum value.
    """
    return electrical_components_pb2.ElectricalComponentCategory.ValueType(
        category.value
    )
