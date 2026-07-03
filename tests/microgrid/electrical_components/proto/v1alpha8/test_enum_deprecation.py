# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for deprecation of the category/type enums and their proto converters."""

import warnings

import pytest
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
    EvChargerType,
    InverterType,
    LiIonBattery,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_category_from_proto,
    electrical_component_category_to_proto,
    electrical_component_class_to_proto,
    ev_charger_type_from_proto,
    ev_charger_type_to_proto,
    inverter_type_from_proto,
    inverter_type_to_proto,
)


def test_electrical_component_category_member_warns() -> None:
    """Accessing an `ElectricalComponentCategory` member must warn."""
    with pytest.deprecated_call():
        _ = ElectricalComponentCategory.BATTERY


def test_inverter_type_member_warns() -> None:
    """Accessing an `InverterType` member must warn."""
    with pytest.deprecated_call():
        _ = InverterType.PV


def test_ev_charger_type_member_warns() -> None:
    """Accessing an `EvChargerType` member must warn."""
    with pytest.deprecated_call():
        _ = EvChargerType.AC


def test_electrical_component_category_to_proto_warns() -> None:
    """Calling `electrical_component_category_to_proto` must warn."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        member = ElectricalComponentCategory.BATTERY
    with pytest.deprecated_call():
        _ = electrical_component_category_to_proto(member)


def test_electrical_component_category_from_proto_warns() -> None:
    """Calling `electrical_component_category_from_proto` must warn."""
    with pytest.deprecated_call():
        _ = electrical_component_category_from_proto(
            electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY
        )


def test_inverter_type_to_proto_warns() -> None:
    """Calling `inverter_type_to_proto` must warn."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        member = InverterType.PV
    with pytest.deprecated_call():
        _ = inverter_type_to_proto(member)


def test_inverter_type_from_proto_warns() -> None:
    """Calling `inverter_type_from_proto` must warn."""
    with pytest.deprecated_call():
        _ = inverter_type_from_proto(electrical_components_pb2.INVERTER_TYPE_PV)


def test_ev_charger_type_to_proto_warns() -> None:
    """Calling `ev_charger_type_to_proto` must warn."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        member = EvChargerType.AC
    with pytest.deprecated_call():
        _ = ev_charger_type_to_proto(member)


def test_ev_charger_type_from_proto_warns() -> None:
    """Calling `ev_charger_type_from_proto` must warn."""
    with pytest.deprecated_call():
        _ = ev_charger_type_from_proto(electrical_components_pb2.EV_CHARGER_TYPE_AC)


def test_class_to_proto_does_not_warn() -> None:
    """The non-deprecated `electrical_component_class_to_proto` must NOT warn."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        result = electrical_component_class_to_proto(LiIonBattery)
    assert result == (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
        electrical_components_pb2.BATTERY_TYPE_LI_ION,
    )
