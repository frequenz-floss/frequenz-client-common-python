# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component categories."""

from __future__ import annotations

import enum

# pylint: disable=no-name-in-module
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentCategory as PBElectricalComponentCategory,
)
from typing_extensions import deprecated

# pylint: enable=no-name-in-module


@enum.unique
class ElectricalComponentCategory(enum.Enum):
    """Possible types of microgrid electrical component."""

    UNSPECIFIED = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_UNSPECIFIED
    """An unknown component category.

    Useful for error handling, and marking unknown components in
    a list of components with otherwise known categories.
    """

    GRID_CONNECTION_POINT = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_GRID_CONNECTION_POINT
    )
    """The point where the local microgrid is connected to the grid."""

    METER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_METER
    """A meter, for measuring electrical metrics, e.g., current, voltage, etc."""

    INVERTER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER
    """An electricity generator, with batteries or solar energy."""

    CONVERTER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_CONVERTER
    """An electricity converter, e.g., a DC-DC converter."""

    BATTERY = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY
    """A storage system for electrical energy, used by inverters."""

    EV_CHARGER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER
    """A station for charging electrical vehicles."""

    CRYPTO_MINER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_CRYPTO_MINER
    """A device for mining cryptocurrencies."""

    ELECTROLYZER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_ELECTROLYZER
    """A device for splitting water into hydrogen and oxygen using electricity."""

    CHP = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_CHP
    """A heat and power combustion plant (CHP stands for combined heat and power)."""

    BREAKER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_BREAKER
    """A relay, used for switching electrical circuits on and off."""

    PRECHARGER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_PRECHARGER
    """A precharger, used for preparing electrical circuits for switching on."""

    POWER_TRANSFORMER = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_POWER_TRANSFORMER
    )
    """A transformer, used for changing the voltage of electrical circuits."""

    HVAC = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_HVAC
    """A heating, ventilation, and air conditioning (HVAC) system."""

    PLC = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_PLC
    """A programmable logic controller (PLC)."""

    STATIC_TRANSFER_SWITCH = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_STATIC_TRANSFER_SWITCH
    )
    """A static transfer switch, used for switching between power sources."""

    UNINTERRUPTIBLE_POWER_SUPPLY = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_UNINTERRUPTIBLE_POWER_SUPPLY
    )
    """An uninterruptible power supply (UPS), used to provide backup power."""

    CAPACITOR_BANK = (
        electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_CAPACITOR_BANK
    )
    """A capacitor bank, used for power factor correction and reactive power compensation."""

    WIND_TURBINE = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_WIND_TURBINE
    """A wind turbine, used to generate electricity from wind energy."""

    STEAM_BOILER = electrical_components_pb2.ELECTRICAL_COMPONENT_CATEGORY_STEAM_BOILER
    """A steam boiler, used to generate steam for heating or industrial processes."""

    @classmethod
    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentCategory.from_proto() is deprecated. "
        "Use frequenz.client.common.microgrid.electrical_components.proto."
        "v1alpha8.electrical_component_category_from_proto instead."
    )
    def from_proto(
        cls, component_category: PBElectricalComponentCategory.ValueType
    ) -> ElectricalComponentCategory:
        """Convert a protobuf ElectricalComponentCategory message to enum.

        Args:
            component_category: protobuf enum to convert

        Returns:
            Enum value corresponding to the protobuf message.
        """
        if not any(t.value == component_category for t in ElectricalComponentCategory):
            return ElectricalComponentCategory.UNSPECIFIED
        return cls(component_category)

    @deprecated(
        "frequenz.client.common.microgrid.electrical_components."
        "ElectricalComponentCategory.to_proto() is deprecated. "
        "Use frequenz.client.common.microgrid.electrical_components.proto."
        "v1alpha8.electrical_component_category_to_proto instead."
    )
    def to_proto(self) -> PBElectricalComponentCategory.ValueType:
        """Convert a ElectricalComponentCategory enum to protobuf message.

        Returns:
            Enum value corresponding to the protobuf message.
        """
        return PBElectricalComponentCategory.ValueType(self.value)
