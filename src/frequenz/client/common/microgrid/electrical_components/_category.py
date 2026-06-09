# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component categories."""

from __future__ import annotations

import enum

# pylint: disable=no-name-in-module
from frequenz.api.common.v1alpha8.microgrid.electrical_components.electrical_components_pb2 import (
    ElectricalComponentCategory as PBElectricalComponentCategory,
)
from typing_extensions import deprecated

# pylint: enable=no-name-in-module


@enum.unique
class ElectricalComponentCategory(enum.Enum):
    """Possible types of microgrid electrical component."""

    UNSPECIFIED = 0
    """An unknown component category.

    Useful for error handling, and marking unknown components in
    a list of components with otherwise known categories.
    """

    GRID_CONNECTION_POINT = 1
    """The point where the local microgrid is connected to the grid."""

    METER = 2
    """A meter, for measuring electrical metrics, e.g., current, voltage, etc."""

    INVERTER = 3
    """An electricity generator, with batteries or solar energy."""

    CONVERTER = 4
    """An electricity converter, e.g., a DC-DC converter."""

    BATTERY = 5
    """A storage system for electrical energy, used by inverters."""

    EV_CHARGER = 6
    """A station for charging electrical vehicles."""

    BREAKER = 7
    """A relay, used for switching electrical circuits on and off."""

    PRECHARGER = 8
    """A precharger, used for preparing electrical circuits for switching on."""

    CHP = 9
    """A heat and power combustion plant (CHP stands for combined heat and power)."""

    ELECTROLYZER = 10
    """A device for splitting water into hydrogen and oxygen using electricity."""

    POWER_TRANSFORMER = 11
    """A transformer, used for changing the voltage of electrical circuits."""

    HVAC = 12
    """A heating, ventilation, and air conditioning (HVAC) system."""

    PLC = 13
    """A programmable logic controller (PLC)."""

    CRYPTO_MINER = 14
    """A device for mining cryptocurrencies."""

    STATIC_TRANSFER_SWITCH = 15
    """A static transfer switch, used for switching between power sources."""

    UNINTERRUPTIBLE_POWER_SUPPLY = 16
    """An uninterruptible power supply (UPS), used to provide backup power."""

    CAPACITOR_BANK = 17
    """A capacitor bank, used for power factor correction and reactive power compensation."""

    WIND_TURBINE = 18
    """A wind turbine, used to generate electricity from wind energy."""

    STEAM_BOILER = 19
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
