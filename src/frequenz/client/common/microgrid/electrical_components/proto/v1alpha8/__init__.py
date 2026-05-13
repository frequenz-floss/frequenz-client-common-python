# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component enums from/to protobuf v1alpha8."""

from ._electrical_component import (
    electrical_component_category_from_proto,
    electrical_component_category_to_proto,
    electrical_component_diagnostic_code_from_proto,
    electrical_component_diagnostic_code_to_proto,
    electrical_component_state_code_from_proto,
    electrical_component_state_code_to_proto,
)

__all__ = [
    "electrical_component_category_from_proto",
    "electrical_component_category_to_proto",
    "electrical_component_diagnostic_code_from_proto",
    "electrical_component_diagnostic_code_to_proto",
    "electrical_component_state_code_from_proto",
    "electrical_component_state_code_to_proto",
]
