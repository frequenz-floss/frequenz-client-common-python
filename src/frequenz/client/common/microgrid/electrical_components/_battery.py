# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Battery electrical component."""

import dataclasses
from typing import Any, Self, TypeAlias

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Battery(ElectricalComponent):
    """An abstract battery electrical component."""

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is Battery:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnspecifiedBattery(Battery):
    """A battery of an unspecified type."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class LiIonBattery(Battery):
    """A Li-ion battery."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class NaIonBattery(Battery):
    """A Na-ion battery."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedBattery(Battery):
    """A battery of an unrecognized type."""

    type: int
    """The raw type of this battery, not recognized by this library version."""


BatteryTypes: TypeAlias = (
    LiIonBattery | NaIonBattery | UnrecognizedBattery | UnspecifiedBattery
)
"""All possible battery types."""
