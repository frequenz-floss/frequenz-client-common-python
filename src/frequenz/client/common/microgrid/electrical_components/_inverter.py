# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Inverter electrical component."""

import dataclasses
from typing import Any, Self, TypeAlias

from ._electrical_component import ElectricalComponent
from ._problematic import ProblematicElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Inverter(ElectricalComponent):
    """An abstract inverter electrical component."""

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is Inverter:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnspecifiedInverter(Inverter, ProblematicElectricalComponent):
    """An inverter of an unspecified type."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class BatteryInverter(Inverter):
    """A battery inverter."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class PvInverter(Inverter):
    """A PV inverter."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class HybridInverter(Inverter):
    """A hybrid inverter."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedInverter(Inverter, ProblematicElectricalComponent):
    """An inverter of an unrecognized type."""

    type: int
    """The raw type of this inverter, not recognized by this library version."""


InverterTypes: TypeAlias = (
    UnspecifiedInverter
    | BatteryInverter
    | PvInverter
    | HybridInverter
    | UnrecognizedInverter
)
"""All possible inverter types."""
