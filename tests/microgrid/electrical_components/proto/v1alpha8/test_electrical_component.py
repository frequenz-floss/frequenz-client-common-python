# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for electrical component enum to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
    ElectricalComponentDiagnosticCode,
    ElectricalComponentStateCode,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_category_from_proto,
    electrical_component_category_to_proto,
    electrical_component_diagnostic_code_from_proto,
    electrical_component_diagnostic_code_to_proto,
    electrical_component_state_code_from_proto,
    electrical_component_state_code_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestElectricalComponentCategoryParity(EnumParityTest):
    """Parity tests for the `ElectricalComponentCategory` enum."""

    python_enum = ElectricalComponentCategory
    proto_enum = electrical_components_pb2.ElectricalComponentCategory
    name_prefix = "ELECTRICAL_COMPONENT_CATEGORY_"
    from_proto = staticmethod(electrical_component_category_from_proto)
    to_proto = staticmethod(electrical_component_category_to_proto)


class TestElectricalComponentStateCodeParity(EnumParityTest):
    """Parity tests for the `ElectricalComponentStateCode` enum."""

    python_enum = ElectricalComponentStateCode
    proto_enum = electrical_components_pb2.ElectricalComponentStateCode
    name_prefix = "ELECTRICAL_COMPONENT_STATE_CODE_"
    from_proto = staticmethod(electrical_component_state_code_from_proto)
    to_proto = staticmethod(electrical_component_state_code_to_proto)


class TestElectricalComponentDiagnosticCodeParity(EnumParityTest):
    """Parity tests for the `ElectricalComponentDiagnosticCode` enum."""

    python_enum = ElectricalComponentDiagnosticCode
    proto_enum = electrical_components_pb2.ElectricalComponentDiagnosticCode
    name_prefix = "ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_"
    from_proto = staticmethod(electrical_component_diagnostic_code_from_proto)
    to_proto = staticmethod(electrical_component_diagnostic_code_to_proto)
