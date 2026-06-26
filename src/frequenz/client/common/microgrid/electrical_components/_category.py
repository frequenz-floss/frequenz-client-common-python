# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component categories."""

import typing_extensions
from frequenz.core.enum import Enum, deprecated_member, unique

_DEPRECATION_MESSAGE = (
    "ElectricalComponentCategory is deprecated; use the ElectricalComponent class "
    "hierarchy (isinstance) or electrical_component_class_to_proto()/"
    "electrical_component_class_from_proto()."
)


def _member_message(name: str) -> str:
    """Build the deprecation message for a specific enum member.

    Args:
        name: The enum member name.

    Returns:
        The full deprecation message for that member.
    """
    return (
        f"ElectricalComponentCategory.{name} is deprecated; use the "
        "ElectricalComponent class hierarchy (isinstance) or "
        "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
    )


@typing_extensions.deprecated(_DEPRECATION_MESSAGE)
@unique
class ElectricalComponentCategory(Enum):
    """Possible types of microgrid electrical component."""

    UNSPECIFIED = deprecated_member(0, _member_message("UNSPECIFIED"))
    """The component category is unspecified. This should not be used."""

    GRID_CONNECTION_POINT = deprecated_member(
        1, _member_message("GRID_CONNECTION_POINT")
    )
    """The point where the local microgrid is connected to the grid."""

    METER = deprecated_member(2, _member_message("METER"))
    """A meter, for measuring electrical metrics, e.g., current, voltage, etc."""

    INVERTER = deprecated_member(3, _member_message("INVERTER"))
    """An inverter that converts DC to AC power and vice versa."""

    CONVERTER = deprecated_member(4, _member_message("CONVERTER"))
    """An electricity converter, e.g., a DC-DC converter."""

    BATTERY = deprecated_member(5, _member_message("BATTERY"))
    """A battery energy storage system."""

    EV_CHARGER = deprecated_member(6, _member_message("EV_CHARGER"))
    """A station for charging electrical vehicles."""

    BREAKER = deprecated_member(7, _member_message("BREAKER"))
    """A circuit breaker, providing protection and switching by disconnecting circuits."""

    PRECHARGER = deprecated_member(8, _member_message("PRECHARGER"))
    """A precharger, used for preparing electrical circuits for switching on."""

    CHP = deprecated_member(9, _member_message("CHP"))
    """A combined heat and power (CHP) plant.

    It generates electricity and useful heat from a single energy source.
    """

    ELECTROLYZER = deprecated_member(10, _member_message("ELECTROLYZER"))
    """A device for splitting water into hydrogen and oxygen using electricity."""

    POWER_TRANSFORMER = deprecated_member(11, _member_message("POWER_TRANSFORMER"))
    """A transformer, used for changing the voltage of electrical circuits."""

    HVAC = deprecated_member(12, _member_message("HVAC"))
    """A heating, ventilation, and air conditioning (HVAC) system."""

    PLC = deprecated_member(13, _member_message("PLC"))
    """A programmable logic controller (PLC)."""

    CRYPTO_MINER = deprecated_member(14, _member_message("CRYPTO_MINER"))
    """A device for mining cryptocurrencies."""

    STATIC_TRANSFER_SWITCH = deprecated_member(
        15, _member_message("STATIC_TRANSFER_SWITCH")
    )
    """A static transfer switch, used for switching between power sources."""

    UNINTERRUPTIBLE_POWER_SUPPLY = deprecated_member(
        16, _member_message("UNINTERRUPTIBLE_POWER_SUPPLY")
    )
    """An uninterruptible power supply (UPS), used to provide backup power."""

    CAPACITOR_BANK = deprecated_member(17, _member_message("CAPACITOR_BANK"))
    """A capacitor bank, used for power factor correction and reactive power compensation."""

    WIND_TURBINE = deprecated_member(18, _member_message("WIND_TURBINE"))
    """A wind turbine, used to generate electricity from wind energy."""

    STEAM_BOILER = deprecated_member(19, _member_message("STEAM_BOILER"))
    """A steam boiler, used to generate steam for heating or industrial processes."""
