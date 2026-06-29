# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component diagnostic codes to/from protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from .....proto import enum_from_proto
from ... import ElectricalComponentDiagnosticCode


def electrical_component_diagnostic_code_from_proto(
    message: electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType,
) -> ElectricalComponentDiagnosticCode | int:
    """Convert a protobuf `ElectricalComponentDiagnosticCode` value to an enum member.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding
            [`ElectricalComponentDiagnosticCode`][....ElectricalComponentDiagnosticCode]
            enum member, or the raw [`int`][] if the protobuf value is not recognized.
    """
    return enum_from_proto(message, ElectricalComponentDiagnosticCode)


def electrical_component_diagnostic_code_to_proto(
    diagnostic_code: ElectricalComponentDiagnosticCode,
) -> electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType:
    """Convert an `ElectricalComponentDiagnosticCode` enum member to a protobuf value.

    Args:
        diagnostic_code: The
            [`ElectricalComponentDiagnosticCode`][....ElectricalComponentDiagnosticCode]
            enum member to convert.

    Returns:
        The corresponding protobuf `ElectricalComponentDiagnosticCode` value.
    """
    return electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType(
        diagnostic_code.value
    )
