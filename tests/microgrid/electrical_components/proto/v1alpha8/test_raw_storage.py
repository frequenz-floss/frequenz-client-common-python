# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the raw category/type values carried by problematic components."""

import dataclasses
import warnings

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
    LiIonBattery,
    UnrecognizedBattery,
    UnrecognizedElectricalComponent,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_class_to_proto,
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


def test_raw_category_preserved_for_unknown(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """An unknown category is preserved as the raw int."""
    base_data = default_component_base_data._replace(category=999)
    component = electrical_component_from_proto(base_data_as_proto(base_data))
    assert isinstance(component, UnrecognizedElectricalComponent)
    assert component.category == 999
    assert electrical_component_class_to_proto(component) == (999, None)


def test_raw_type_preserved_for_unknown(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """An unknown battery type is preserved as the raw int."""
    component = UnrecognizedBattery(
        id=default_component_base_data.component_id,
        microgrid_id=default_component_base_data.microgrid_id,
        name="",
        model=default_component_base_data.model,
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )
    assert component.type == 999
    assert electrical_component_class_to_proto(component) == (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
        999,
    )


def test_recognized_classes_carry_no_category_or_type(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """Recognized classes have no category/type attributes or repr entries."""
    battery = _li_ion_battery(default_component_base_data)
    assert not hasattr(battery, "category")
    assert not hasattr(battery, "type")
    text = repr(battery)
    assert "category=" not in text
    assert "type=" not in text


def test_unrecognized_type_shows_in_repr(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """The raw type of an unrecognized component shows up in repr()."""
    component = UnrecognizedBattery(
        id=default_component_base_data.component_id,
        microgrid_id=default_component_base_data.microgrid_id,
        name="",
        model=default_component_base_data.model,
        type=999,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )
    assert "type=999" in repr(component)


def test_type_participates_in_equality_and_hash(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """The raw type is part of equality and hashing."""

    def _unrecognized_battery(battery_type: int) -> UnrecognizedBattery:
        return UnrecognizedBattery(
            id=default_component_base_data.component_id,
            microgrid_id=default_component_base_data.microgrid_id,
            name="",
            model=default_component_base_data.model,
            type=battery_type,
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


def test_replace_preserves_class(
    default_component_base_data: _ElectricalComponentBaseData,
) -> None:
    """`dataclasses.replace` keeps the class and thus the proto identity."""
    battery = _li_ion_battery(default_component_base_data)
    replaced = dataclasses.replace(battery, name="renamed")
    assert isinstance(replaced, LiIonBattery)
    assert replaced.name == "renamed"
    assert electrical_component_class_to_proto(replaced) == (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
        electrical_components_pb2.BATTERY_TYPE_LI_ION,
    )


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
