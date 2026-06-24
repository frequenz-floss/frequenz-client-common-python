# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for EV charger type to/from protobuf v1alpha8 conversion."""

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import EvChargerType
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    ev_charger_type_from_proto,
    ev_charger_type_to_proto,
)
from frequenz.client.common.test.enum_parity import EnumParityTest


class TestEvChargerTypeParity(EnumParityTest):
    """Parity tests for the `EvChargerType` enum."""

    python_enum = EvChargerType
    proto_enum = electrical_components_pb2.EvChargerType
    name_prefix = "EV_CHARGER_TYPE_"
    from_proto = staticmethod(ev_charger_type_from_proto)
    to_proto = staticmethod(ev_charger_type_to_proto)
    deprecated_members = frozenset(m.name for m in EvChargerType)
    silence_deprecations = True
