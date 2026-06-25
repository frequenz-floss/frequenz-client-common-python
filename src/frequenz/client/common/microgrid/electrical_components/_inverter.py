# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Inverter electrical component."""

import dataclasses
import enum
import warnings
from typing import Any, Self, TypeAlias

import typing_extensions

from ._electrical_component import ElectricalComponent


@enum.unique
class InverterType(enum.Enum):
    """The known types of inverters."""

    UNSPECIFIED = 0
    """The type of the inverter is unspecified."""

    BATTERY = 1
    """The inverter is a battery inverter."""

    PV = 2
    """The inverter is a PV inverter."""

    HYBRID = 3
    """The inverter is a hybrid inverter."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class Inverter(ElectricalComponent):
    """An abstract inverter electrical component."""

    _category: int = dataclasses.field(
        default=3, repr=False
    )  # ElectricalComponentCategory.INVERTER
    """The category of this electrical component.

    Note:
        This should not be used normally, you should test if an electrical component
        [`isinstance`][] of a concrete electrical component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about a new category yet (i.e. for use with
        [`UnrecognizedElectricalComponent`][...UnrecognizedElectricalComponent]) and in
        case some low level code needs to know the category of an electrical component.
    """

    _type: int = dataclasses.field(repr=False)
    """The type of this inverter.

    Note:
        This should not be used normally, you should test if an inverter
        [`isinstance`][] of a concrete inverter class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new inverter type yet (i.e. for use with
        [`UnrecognizedInverter`][...UnrecognizedInverter]).
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is Inverter:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)

    @property
    @typing_extensions.deprecated(
        "InverterType is deprecated; identify inverters via isinstance() on the "
        "class hierarchy, or convert with "
        "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
    )
    def type(self) -> InverterType | int:
        """The deprecated type of this inverter."""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            try:
                return InverterType(self._type)
            except ValueError:
                return self._type


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnspecifiedInverter(Inverter):
    """An inverter of an unspecified type."""

    _type: int = dataclasses.field(default=0, repr=False)  # InverterType.UNSPECIFIED
    """The type of this inverter.

    Note:
        This should not be used normally, you should test if an inverter
        [`isinstance`][] of a concrete inverter class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new inverter type yet (i.e. for use with
        [`UnrecognizedInverter`][...UnrecognizedInverter]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class BatteryInverter(Inverter):
    """A battery inverter."""

    _type: int = dataclasses.field(default=1, repr=False)  # InverterType.BATTERY
    """The type of this inverter.

    Note:
        This should not be used normally, you should test if an inverter
        [`isinstance`][] of a concrete inverter class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new inverter type yet (i.e. for use with
        [`UnrecognizedInverter`][...UnrecognizedInverter]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class PvInverter(Inverter):
    """A PV inverter."""

    _type: int = dataclasses.field(default=2, repr=False)  # InverterType.PV
    """The type of this inverter.

    Note:
        This should not be used normally, you should test if an inverter
        [`isinstance`][] of a concrete inverter class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new inverter type yet (i.e. for use with
        [`UnrecognizedInverter`][...UnrecognizedInverter]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class HybridInverter(Inverter):
    """A hybrid inverter."""

    _type: int = dataclasses.field(default=3, repr=False)  # InverterType.HYBRID
    """The type of this inverter.

    Note:
        This should not be used normally, you should test if an inverter
        [`isinstance`][] of a concrete inverter class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new inverter type yet (i.e. for use with
        [`UnrecognizedInverter`][...UnrecognizedInverter]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedInverter(Inverter):
    """An inverter of an unrecognized type."""

    _type: int = dataclasses.field(repr=False)
    """The unrecognized type of this inverter."""

    @property
    @typing_extensions.override
    def type(self) -> int:
        """The deprecated type of this inverter."""
        return self._type


InverterTypes: TypeAlias = (
    UnspecifiedInverter
    | BatteryInverter
    | PvInverter
    | HybridInverter
    | UnrecognizedInverter
)
"""All possible inverter types."""
