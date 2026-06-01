# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component enums to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import (
    ElectricalComponentCategory,
    ElectricalComponentDiagnosticCode,
    ElectricalComponentStateCode,
)


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


def electrical_component_state_code_from_proto(
    message: electrical_components_pb2.ElectricalComponentStateCode.ValueType,
) -> ElectricalComponentStateCode | int:
    """Convert a protobuf ElectricalComponentStateCode enum value to an enum member.

    Args:
        message: A protobuf ElectricalComponentStateCode enum value.

    Returns:
        The corresponding ElectricalComponentStateCode enum member, or the raw `int`
            if the protobuf value is not recognized.
    """
    return enum_from_proto(message, ElectricalComponentStateCode)


def electrical_component_state_code_to_proto(
    state_code: ElectricalComponentStateCode,
) -> electrical_components_pb2.ElectricalComponentStateCode.ValueType:
    """Convert an ElectricalComponentStateCode enum member to a protobuf enum value.

    Args:
        state_code: An ElectricalComponentStateCode enum member.

    Returns:
        The corresponding protobuf ElectricalComponentStateCode enum value.
    """
    return electrical_components_pb2.ElectricalComponentStateCode.ValueType(
        state_code.value
    )


def electrical_component_diagnostic_code_from_proto(
    message: electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType,
) -> ElectricalComponentDiagnosticCode | int:
    """Convert a protobuf ElectricalComponentDiagnosticCode value to an enum member.

    Args:
        message: A protobuf ElectricalComponentDiagnosticCode enum value.

    Returns:
        The corresponding ElectricalComponentDiagnosticCode enum member, or the raw
            `int` if the protobuf value is not recognized.
    """
    return enum_from_proto(message, ElectricalComponentDiagnosticCode)


def electrical_component_diagnostic_code_to_proto(
    diagnostic_code: ElectricalComponentDiagnosticCode,
) -> electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType:
    """Convert an ElectricalComponentDiagnosticCode enum member to a protobuf value.

    Args:
        diagnostic_code: An ElectricalComponentDiagnosticCode enum member.

    Returns:
        The corresponding protobuf ElectricalComponentDiagnosticCode enum value.
    """
    return electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType(
        diagnostic_code.value
    )
