# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Electric vehicle (EV) charger electrical component."""

import dataclasses
from typing import Any, Self, TypeAlias

import typing_extensions
from frequenz.core.enum import Enum, deprecated_member, unique

from ._electrical_component import ElectricalComponent

_EV_CHARGER_TYPE_DEPRECATION_MESSAGE = (
    "EvChargerType is deprecated; identify EV chargers via isinstance() on the "
    "class hierarchy, or convert with "
    "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
)


def _ev_charger_type_member_message(name: str) -> str:
    """Build the deprecation message for a specific `EvChargerType` member.

    Args:
        name: The enum member name.

    Returns:
        The full deprecation message for that member.
    """
    return (
        f"EvChargerType.{name} is deprecated; identify EV chargers via isinstance() "
        "on the class hierarchy, or convert with "
        "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
    )


@typing_extensions.deprecated(_EV_CHARGER_TYPE_DEPRECATION_MESSAGE)
@unique
class EvChargerType(Enum):
    """The known types of electric vehicle (EV) chargers."""

    UNSPECIFIED = deprecated_member(0, _ev_charger_type_member_message("UNSPECIFIED"))
    """The type of the EV charger is unspecified."""

    AC = deprecated_member(1, _ev_charger_type_member_message("AC"))
    """The EV charging station supports AC charging only."""

    DC = deprecated_member(2, _ev_charger_type_member_message("DC"))
    """The EV charging station supports DC charging only."""

    HYBRID = deprecated_member(3, _ev_charger_type_member_message("HYBRID"))
    """The EV charging station supports both AC and DC."""


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
class UnspecifiedEvCharger(EvCharger):
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
class UnrecognizedEvCharger(EvCharger):
    """An EV charger of an unrecognized type."""

    type: int
    """The raw type of this EV charger, not recognized by this library version."""


EvChargerTypes: TypeAlias = (
    UnspecifiedEvCharger
    | AcEvCharger
    | DcEvCharger
    | HybridEvCharger
    | UnrecognizedEvCharger
)
"""All possible EV charger types."""
