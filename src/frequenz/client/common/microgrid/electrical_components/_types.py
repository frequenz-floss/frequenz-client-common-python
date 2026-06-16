# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""All known component types."""

from typing import TypeAlias

from ._battery import BatteryTypes, UnrecognizedBattery, UnspecifiedBattery
from ._breaker import Breaker
from ._chp import Chp
from ._converter import Converter
from ._crypto_miner import CryptoMiner
from ._electrolyzer import Electrolyzer
from ._ev_charger import EvChargerTypes, UnrecognizedEvCharger, UnspecifiedEvCharger
from ._grid_connection_point import GridConnectionPoint
from ._hvac import Hvac
from ._inverter import InverterTypes, UnrecognizedInverter, UnspecifiedInverter
from ._meter import Meter
from ._power_transformer import PowerTransformer
from ._precharger import Precharger
from ._problematic import (
    MismatchedCategoryElectricalComponent,
    UnrecognizedElectricalComponent,
    UnspecifiedElectricalComponent,
)
from ._steam_boiler import SteamBoiler
from ._wind_turbine import WindTurbine

UnspecifiedElectricalComponentTypes: TypeAlias = (
    UnspecifiedBattery
    | UnspecifiedElectricalComponent
    | UnspecifiedEvCharger
    | UnspecifiedInverter
)
"""All unspecified electrical component types."""

UnrecognizedElectricalComponentTypes: TypeAlias = (
    UnrecognizedBattery
    | UnrecognizedElectricalComponent
    | UnrecognizedEvCharger
    | UnrecognizedInverter
)

ProblematicElectricalComponentTypes: TypeAlias = (
    MismatchedCategoryElectricalComponent
    | UnrecognizedElectricalComponentTypes
    | UnspecifiedElectricalComponentTypes
)
"""All possible electrical component types that have a problem."""

ComponentTypes: TypeAlias = (
    BatteryTypes
    | Breaker
    | Chp
    | Converter
    | CryptoMiner
    | Electrolyzer
    | EvChargerTypes
    | GridConnectionPoint
    | Hvac
    | InverterTypes
    | Meter
    | PowerTransformer
    | Precharger
    | ProblematicElectricalComponentTypes
    | SteamBoiler
    | WindTurbine
)
"""All possible component types."""
