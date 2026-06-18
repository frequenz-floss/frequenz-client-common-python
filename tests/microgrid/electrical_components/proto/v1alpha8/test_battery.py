# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for battery type to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import BatteryType
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    battery_type_from_proto,
    battery_type_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestBatteryTypeParity(EnumParityTest):
    """Parity tests for the `BatteryType` enum."""

    python_enum = BatteryType
    proto_enum = electrical_components_pb2.BatteryType
    name_prefix = "BATTERY_TYPE_"
    from_proto = staticmethod(battery_type_from_proto)
    to_proto = staticmethod(battery_type_to_proto)
