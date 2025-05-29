# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Defines the electrical components that can be used in a microgrid."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from frequenz.api.common.v1.microgrid.electrical_components import (
    electrical_components_pb2,
    grid_pb2,
    inverter_pb2,
)

from ..id import ComponentId, MicrogridId


class ComponentType(Enum):
    """A base class from which individual component types are derived."""


class InverterType(ComponentType):
    """Enum representing inverter types."""

    NONE = inverter_pb2.InverterType.TYPE_UNSPECIFIED
    """Unspecified inverter type."""

    BATTERY = inverter_pb2.InverterType.TYPE_BATTERY
    """Battery inverter."""

    SOLAR = inverter_pb2.InverterType.TYPE_SOLAR
    """Solar inverter."""

    HYBRID = inverter_pb2.InverterType.TYPE_HYBRID
    """Hybrid inverter."""


def component_type_from_protobuf(
    component_category: electrical_components_pb2.ElectricalComponentCategory.ValueType,
    component_metadata: inverter_pb2.Inverter,
) -> ComponentType | None:
    """Convert a protobuf InverterType message to Component enum.

    For internal-only use by the `microgrid` package.

    Args:
        component_category: category the type belongs to.
        component_metadata: protobuf metadata to fetch type from.

    Returns:
        Enum value corresponding to the protobuf message.
    """
    # ComponentType values in the protobuf definition are not unique across categories
    # as of v0.11.0, so we need to check the component category first, before doing any
    # component type checks.
    if (
        component_category
        == electrical_components_pb2.ElectricalComponentCategory.COMPONENT_CATEGORY_INVERTER
    ):
        if not any(int(t.value) == int(component_metadata.type) for t in InverterType):
            return None

        return InverterType(component_metadata.type)

    return None


class ElectricalComponentCategory(Enum):
    """Possible types of microgrid electrical component."""

    UNSPECIFIED = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_UNSPECIFIED
    )
    """An unknown component category.

    Useful for error handling, and marking unknown components in
    a list of components with otherwise known categories.
    """

    GRID = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_GRID
    )
    """The point where the local microgrid is connected to the grid."""

    METER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_METER
    )
    """A meter, for measuring electrical metrics, e.g., current, voltage, etc."""

    INVERTER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_INVERTER
    )
    """An electricity generator, with batteries or solar energy."""

    CONVERTER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_CONVERTER
    )
    """An electricity converter, e.g., a DC-DC converter."""

    BATTERY = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_BATTERY
    )
    """A storage system for electrical energy, used by inverters."""

    EV_CHARGER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER
    )
    """A station for charging electrical vehicles."""

    CRYPTO_MINER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_CRYPTO_MINER
    )
    """A device for mining cryptocurrencies."""

    ELECTROLYZER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_ELECTROLYZER
    )
    """A device for splitting water into hydrogen and oxygen using electricity."""

    CHP = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_CHP
    )
    """A heat and power combustion plant (CHP stands for combined heat and power)."""

    RELAY = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_RELAY
    )
    """A relay, used for switching electrical circuits on and off."""

    PRECHARGER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_PRECHARGER
    )
    """A precharger, used for preparing electrical circuits for switching on."""

    FUSE = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_FUSE
    )
    """A fuse, used for protecting electrical circuits from overcurrent."""

    TRANSFORMER = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_VOLTAGE_TRANSFORMER
    )
    """A transformer, used for changing the voltage of electrical circuits."""

    HVAC = (
        electrical_components_pb2.ElectricalComponentCategory.ELECTRICAL_COMPONENT_CATEGORY_HVAC
    )
    """A heating, ventilation, and air conditioning (HVAC) system."""


def component_category_from_protobuf(
    component_category: electrical_components_pb2.ElectricalComponentCategory.ValueType,
) -> ElectricalComponentCategory:
    """Convert a protobuf ElectricalComponentCategory message to ElectricalComponentCategory enum.

    For internal-only use by the `microgrid` package.

    Args:
        component_category: protobuf enum to convert

    Returns:
        Enum value corresponding to the protobuf message.
    """
    if not any(t.value == component_category for t in ElectricalComponentCategory):
        return ElectricalComponentCategory.UNSPECIFIED

    return ElectricalComponentCategory(component_category)


@dataclass(frozen=True)
class Fuse:
    """Fuse data class."""

    max_current: float
    """Rated current of the fuse."""


@dataclass(frozen=True)
class ComponentMetadata:
    """Base class for component metadata classes."""

    fuse: Fuse | None = None
    """The fuse at the grid connection point."""


@dataclass(frozen=True)
class GridMetadata(ComponentMetadata):
    """Metadata for a grid connection point."""


def component_metadata_from_protobuf(
    component_category: electrical_components_pb2.ElectricalComponentCategory.ValueType,
    component_metadata: grid_pb2.GridConnectionPoint,
) -> GridMetadata | None:
    """Convert a protobuf GridMetadata message to GridMetadata class.

    Args:
        component_category: category the type belongs to.
        component_metadata: protobuf metadata to fetch type from.

    Returns:
        GridMetadata instance corresponding to the protobuf message.
    """
    if (
        component_category
        == electrical_components_pb2.ElectricalComponentCategory.COMPONENT_CATEGORY_GRID
    ):
        max_current = component_metadata.rated_fuse_current
        fuse = Fuse(max_current)
        return GridMetadata(fuse)

    return None


class ComponentMetricId(Enum):
    """An enum representing the various metrics available in the microgrid."""

    ACTIVE_POWER = "active_power"
    """Active power."""

    ACTIVE_POWER_PHASE_1 = "active_power_phase_1"
    """Active power in phase 1."""
    ACTIVE_POWER_PHASE_2 = "active_power_phase_2"
    """Active power in phase 2."""
    ACTIVE_POWER_PHASE_3 = "active_power_phase_3"
    """Active power in phase 3."""

    REACTIVE_POWER = "reactive_power"
    """Reactive power."""

    REACTIVE_POWER_PHASE_1 = "reactive_power_phase_1"
    """Reactive power in phase 1."""
    REACTIVE_POWER_PHASE_2 = "reactive_power_phase_2"
    """Reactive power in phase 2."""
    REACTIVE_POWER_PHASE_3 = "reactive_power_phase_3"
    """Reactive power in phase 3."""

    CURRENT_PHASE_1 = "current_phase_1"
    """Current in phase 1."""
    CURRENT_PHASE_2 = "current_phase_2"
    """Current in phase 2."""
    CURRENT_PHASE_3 = "current_phase_3"
    """Current in phase 3."""

    VOLTAGE_PHASE_1 = "voltage_phase_1"
    """Voltage in phase 1."""
    VOLTAGE_PHASE_2 = "voltage_phase_2"
    """Voltage in phase 2."""
    VOLTAGE_PHASE_3 = "voltage_phase_3"
    """Voltage in phase 3."""

    FREQUENCY = "frequency"

    SOC = "soc"
    """State of charge."""
    SOC_LOWER_BOUND = "soc_lower_bound"
    """Lower bound of state of charge."""
    SOC_UPPER_BOUND = "soc_upper_bound"
    """Upper bound of state of charge."""
    CAPACITY = "capacity"
    """Capacity."""

    POWER_INCLUSION_LOWER_BOUND = "power_inclusion_lower_bound"
    """Power inclusion lower bound."""
    POWER_EXCLUSION_LOWER_BOUND = "power_exclusion_lower_bound"
    """Power exclusion lower bound."""
    POWER_EXCLUSION_UPPER_BOUND = "power_exclusion_upper_bound"
    """Power exclusion upper bound."""
    POWER_INCLUSION_UPPER_BOUND = "power_inclusion_upper_bound"
    """Power inclusion upper bound."""

    ACTIVE_POWER_INCLUSION_LOWER_BOUND = "active_power_inclusion_lower_bound"
    """Active power inclusion lower bound."""
    ACTIVE_POWER_EXCLUSION_LOWER_BOUND = "active_power_exclusion_lower_bound"
    """Active power exclusion lower bound."""
    ACTIVE_POWER_EXCLUSION_UPPER_BOUND = "active_power_exclusion_upper_bound"
    """Active power exclusion upper bound."""
    ACTIVE_POWER_INCLUSION_UPPER_BOUND = "active_power_inclusion_upper_bound"
    """Active power inclusion upper bound."""

    TEMPERATURE = "temperature"
    """Temperature."""


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class ElectricalComponent:
    """Metadata for a single microgrid electrical component."""

    id: ComponentId
    """The ID of this component."""

    microgrid_id: MicrogridId
    """The unique identifier of the microgrid."""

    name: str | None
    """Name of the microgrid."""

    category: ElectricalComponentCategory
    """The category of this component."""

    metadata: ComponentMetadata | None = None
    """The metadata of this component."""

    manufacturer: str | None = None
    """The manufacturer of this component."""

    model: str | None = None
    """The model of this component."""

    status: str | None = None
    """The status of this component, e.g., "active", "inactive", etc."""

    start: datetime | None = None
    """The moment when the component became operationally active."""

    end: datetime | None = None
    """The moment when the component's operational activity ceased."""

    metric_config_bounds: ComponentMetricId | None = None
    """Configuration bounds for the metrics of this component."""

    def is_valid(self) -> bool:
        """Check if this instance contains valid data.

        Returns:
            `True` if `id > 0` and `type` is a valid `ComponentCategory`, or if `id
                == 0` and `type` is `GRID`, `False` otherwise
        """
        return (
            int(self.id) > 0
            and any(t == self.category for t in ElectricalComponentCategory)
        ) or (
            int(self.id) == 0
            and self.category == ElectricalComponentCategory.GRID
        )

    def __hash__(self) -> int:
        """Compute a hash of this instance, obtained by hashing the `component_id` field.

        Returns:
            Hash of this instance.
        """
        return hash(self.id)
