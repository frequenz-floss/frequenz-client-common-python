# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component enums from/to protobuf v1alpha8."""

from ._electrical_component import (
    electrical_component_category_from_proto,
    electrical_component_category_to_proto,
    electrical_component_diagnostic_code_from_proto,
    electrical_component_diagnostic_code_to_proto,
    electrical_component_from_proto,
    electrical_component_from_proto_with_issues,
    electrical_component_state_code_from_proto,
    electrical_component_state_code_to_proto,
)
from ._electrical_component_connection import (
    electrical_component_connection_from_proto,
    electrical_component_connection_from_proto_with_issues,
)

__all__ = [
    "electrical_component_category_from_proto",
    "electrical_component_category_to_proto",
    "electrical_component_connection_from_proto",
    "electrical_component_connection_from_proto_with_issues",
    "electrical_component_diagnostic_code_from_proto",
    "electrical_component_diagnostic_code_to_proto",
    "electrical_component_from_proto",
    "electrical_component_from_proto_with_issues",
    "electrical_component_state_code_from_proto",
    "electrical_component_state_code_to_proto",
]
