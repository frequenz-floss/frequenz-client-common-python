# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component categories."""

import enum


@enum.unique
class ElectricalComponentCategory(enum.Enum):
    """Possible types of microgrid electrical component."""

    UNSPECIFIED = 0
    """The component category is unspecified. This should not be used."""

    GRID_CONNECTION_POINT = 1
    """The point where the local microgrid is connected to the grid."""

    METER = 2
    """A meter, for measuring electrical metrics, e.g., current, voltage, etc."""

    INVERTER = 3
    """An inverter that converts DC to AC power and vice versa."""

    CONVERTER = 4
    """An electricity converter, e.g., a DC-DC converter."""

    BATTERY = 5
    """A battery energy storage system."""

    EV_CHARGER = 6
    """A station for charging electrical vehicles."""

    BREAKER = 7
    """A circuit breaker, providing protection and switching by disconnecting circuits."""

    PRECHARGER = 8
    """A precharger, used for preparing electrical circuits for switching on."""

    CHP = 9
    """A combined heat and power (CHP) plant.

    It generates electricity and useful heat from a single energy source.
    """

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
