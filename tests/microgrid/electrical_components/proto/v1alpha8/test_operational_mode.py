# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for electrical component operational mode to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentOperationalMode,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_operational_mode_from_proto,
    electrical_component_operational_mode_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestElectricalComponentOperationalModeParity(EnumParityTest):
    """Parity tests for the `ElectricalComponentOperationalMode` enum."""

    python_enum = ElectricalComponentOperationalMode
    proto_enum = electrical_components_pb2.ElectricalComponentOperationalMode
    name_prefix = "ELECTRICAL_COMPONENT_OPERATIONAL_MODE_"
    from_proto = staticmethod(electrical_component_operational_mode_from_proto)
    to_proto = staticmethod(electrical_component_operational_mode_to_proto)
