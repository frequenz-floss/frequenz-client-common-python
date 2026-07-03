# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Inverter electrical component."""

import dataclasses
from typing import Any, Self, TypeAlias

import typing_extensions
from frequenz.core.enum import Enum, deprecated_member, unique

from ._electrical_component import ElectricalComponent

_INVERTER_TYPE_DEPRECATION_MESSAGE = (
    "InverterType is deprecated; identify inverters via isinstance() on the "
    "class hierarchy, or convert with "
    "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
)


def _inverter_type_member_message(name: str) -> str:
    """Build the deprecation message for a specific `InverterType` member.

    Args:
        name: The enum member name.

    Returns:
        The full deprecation message for that member.
    """
    return (
        f"InverterType.{name} is deprecated; identify inverters via isinstance() "
        "on the class hierarchy, or convert with "
        "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
    )


@typing_extensions.deprecated(_INVERTER_TYPE_DEPRECATION_MESSAGE)
@unique
class InverterType(Enum):
    """The known types of inverters."""

    UNSPECIFIED = deprecated_member(0, _inverter_type_member_message("UNSPECIFIED"))
    """The type of the inverter is unspecified."""

    BATTERY = deprecated_member(1, _inverter_type_member_message("BATTERY"))
    """The inverter is a battery inverter."""

    PV = deprecated_member(2, _inverter_type_member_message("PV"))
    """The inverter is a PV inverter."""

    HYBRID = deprecated_member(3, _inverter_type_member_message("HYBRID"))
    """The inverter is a hybrid inverter."""


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
class UnspecifiedInverter(Inverter):
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
class UnrecognizedInverter(Inverter):
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
