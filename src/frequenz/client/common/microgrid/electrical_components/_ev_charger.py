# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Electric vehicle (EV) charger electrical component."""

import dataclasses
from typing import Any, Self, TypeAlias

from ._electrical_component import ElectricalComponent
from ._problematic import ProblematicElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class EvCharger(ElectricalComponent):
    """An abstract EV charger electrical component."""

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is EvCharger:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnspecifiedEvCharger(EvCharger, ProblematicElectricalComponent):
    """An EV charger of an unspecified type."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class AcEvCharger(EvCharger):
    """An EV charger that supports AC charging only."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class DcEvCharger(EvCharger):
    """An EV charger that supports DC charging only."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class HybridEvCharger(EvCharger):
    """An EV charger that supports both AC and DC charging."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedEvCharger(EvCharger, ProblematicElectricalComponent):
    """An EV charger of an unrecognized type."""

    type: int
    """The raw type of this EV charger, not recognized by this library version."""

    def __str__(self) -> str:
        """Return a string representation exposing the raw type."""
        return f"{self.id}:{self.name}:EvCharger:type={self.type}"


EvChargerTypes: TypeAlias = (
    UnspecifiedEvCharger
    | AcEvCharger
    | DcEvCharger
    | HybridEvCharger
    | UnrecognizedEvCharger
)
"""All possible EV charger types."""
