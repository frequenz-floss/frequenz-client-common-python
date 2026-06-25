# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the deprecated ``category``/``type`` attributes and raw int storage."""

import dataclasses
import warnings

import pytest
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import (
    BatteryType,
    Chp,
    ElectricalComponentCategory,
    LiIonBattery,
    UnrecognizedBattery,
    UnrecognizedElectricalComponent,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_from_proto,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8._electrical_component import (  # noqa: E501
    _ElectricalComponentBaseData,
)

from .conftest import base_data_as_proto


def _li_ion_battery(
    default_component_base_data: _ElectricalComponentBaseData,
) -> LiIonBattery:
    """Build a `LiIonBattery` through the protobuf converter."""
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.BATTERY
    )
    proto = base_data_as_proto(base_data)
    proto.category_specific_info.battery.type = (
        electrical_components_pb2.BATTERY_TYPE_LI_ION
    )
    component = electrical_component_from_proto(proto)
    assert isinstance(component, LiIonBattery)
    return component


def _chp(default_component_base_data: _ElectricalComponentBaseData) -> Chp:
    """Build a `Chp` through the protobuf converter."""
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.CHP
    )
    component = electrical_component_from_proto(base_data_as_proto(base_data))
    assert isinstance(component, Chp)
    return component


def test_category_property_reconstructs_member(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """The deprecated `category` property warns once and rebuilds the member."""
    chp = _chp(default_component_base_data)
    with pytest.warns(DeprecationWarning) as record:
        category = chp.category
    assert category is ElectricalComponentCategory.CHP
    assert len(record) == 1


def test_type_property_reconstructs_member(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """The deprecated `type` property warns once and rebuilds the member."""
    battery = _li_ion_battery(default_component_base_data)
    with pytest.warns(DeprecationWarning) as record:
        battery_type = battery.type
    assert battery_type is BatteryType.LI_ION
    assert len(record) == 1


def test_category_property_returns_raw_int_for_unknown(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """An unknown category is exposed as the raw int via the property."""
    base_data = default_component_base_data._replace(category=999)
    component = electrical_component_from_proto(base_data_as_proto(base_data))
    assert isinstance(component, UnrecognizedElectricalComponent)
    assert component.category == 999


def test_type_property_returns_raw_int_for_unknown(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """An unknown battery type is exposed as the raw int via the property."""
    component = UnrecognizedBattery(
        id=default_component_base_data.component_id,
        microgrid_id=default_component_base_data.microgrid_id,
        _type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )
    assert component.type == 999


def test_raw_storage_not_in_repr(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """Neither the public nor the private category/type names appear in repr()."""
    battery = _li_ion_battery(default_component_base_data)
    text = repr(battery)
    assert "category=" not in text
    assert "_category=" not in text
    assert "type=" not in text
    assert "_type=" not in text


def test_type_participates_in_equality_and_hash(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """The raw type is part of equality and hashing."""

    def _unrecognized_battery(battery_type: int) -> UnrecognizedBattery:
        return UnrecognizedBattery(
            id=default_component_base_data.component_id,
            microgrid_id=default_component_base_data.microgrid_id,
            _type=battery_type,
            _provides_telemetry=True,
            _accepts_control=True,
            _allow_construction=True,
        )

    first = _unrecognized_battery(998)
    second = _unrecognized_battery(999)
    third = _unrecognized_battery(998)

    assert first != second
    assert first == third
    assert hash(first) == hash(third)


def test_replace_preserves_raw_storage(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """`dataclasses.replace` keeps the raw category/type and the class."""
    battery = _li_ion_battery(default_component_base_data)
    replaced = dataclasses.replace(battery, name="renamed")
    assert isinstance(replaced, LiIonBattery)
    assert replaced.name == "renamed"
    with pytest.deprecated_call():
        assert replaced.category is ElectricalComponentCategory.BATTERY
    with pytest.deprecated_call():
        assert replaced.type is BatteryType.LI_ION


def test_from_proto_emits_no_deprecation_warning(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """Converting a protobuf message must not emit a `DeprecationWarning`."""
    base_data = default_component_base_data._replace(
        category=ElectricalComponentCategory.BATTERY
    )
    proto = base_data_as_proto(base_data)
    proto.category_specific_info.battery.type = (
        electrical_components_pb2.BATTERY_TYPE_LI_ION
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        component = electrical_component_from_proto(proto)
    assert isinstance(component, LiIonBattery)
