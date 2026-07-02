# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for inverter type to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import InverterType
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    inverter_type_from_proto,
    inverter_type_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestInverterTypeParity(EnumParityTest):
    """Parity tests for the `InverterType` enum."""

    python_enum = InverterType
    proto_enum = electrical_components_pb2.InverterType
    name_prefix = "INVERTER_TYPE_"
    from_proto = staticmethod(inverter_type_from_proto)
    to_proto = staticmethod(inverter_type_to_proto)
    deprecated_members = frozenset(m.name for m in InverterType)
    silence_deprecations = True
