# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical component enums from/to protobuf v1alpha8."""

from ._category import (
    electrical_component_category_from_proto,
    electrical_component_category_to_proto,
)
from ._diagnostic_code import (
    electrical_component_diagnostic_code_from_proto,
    electrical_component_diagnostic_code_to_proto,
)
from ._electrical_component import (
    AbstractTypedTypes,
    ConcreteTypedTypes,
    ConcreteTypelessTypes,
    ConvertibleElectricalComponentTypes,
    ProtoTypeEnums,
    SpecifiedConcreteTypelessTypes,
    electrical_component_class_from_proto,
    electrical_component_class_to_proto,
    electrical_component_from_proto,
    electrical_component_from_proto_with_issues,
)
from ._electrical_component_connection import (
    electrical_component_connection_from_proto,
)
from ._state_code import (
    electrical_component_state_code_from_proto,
    electrical_component_state_code_to_proto,
)

__all__ = [
    "AbstractTypedTypes",
    "ConcreteTypedTypes",
    "ConcreteTypelessTypes",
    "ConvertibleElectricalComponentTypes",
    "ProtoTypeEnums",
    "SpecifiedConcreteTypelessTypes",
    "electrical_component_category_from_proto",
    "electrical_component_category_to_proto",
    "electrical_component_class_from_proto",
    "electrical_component_class_to_proto",
    "electrical_component_connection_from_proto",
    "electrical_component_diagnostic_code_from_proto",
    "electrical_component_diagnostic_code_to_proto",
    "electrical_component_from_proto",
    "electrical_component_from_proto_with_issues",
    "electrical_component_state_code_from_proto",
    "electrical_component_state_code_to_proto",
]
