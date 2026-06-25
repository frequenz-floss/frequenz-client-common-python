# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Battery electrical component."""

import dataclasses
import enum
import warnings
from typing import Any, Self, TypeAlias

import typing_extensions

from ._electrical_component import ElectricalComponent


@enum.unique
class BatteryType(enum.Enum):
    """The known types of batteries."""

    UNSPECIFIED = 0
    """The battery type is unspecified."""

    LI_ION = 1
    """Lithium-ion (Li-ion) battery."""

    NA_ION = 2
    """Sodium-ion (Na-ion) battery."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class Battery(ElectricalComponent):
    """An abstract battery electrical component."""

    _category: int = dataclasses.field(
        default=5, repr=False
    )  # ElectricalComponentCategory.BATTERY
    """The category of this electrical component.

    Note:
        This should not be used normally, you should test if an electrical
        component [`isinstance`][] of a concrete electrical component class
        instead.

        It is only provided for using with a newer version of the API where
        the client doesn't know about a new category yet (i.e. for use with
        [`UnrecognizedElectricalComponent`][...UnrecognizedElectricalComponent])
        and in case some low level code needs to know the category of an electrical
        component.
    """

    _type: int = dataclasses.field(repr=False)
    """The type of this battery.

    Note:
        This should not be used normally, you should test if a battery
        [`isinstance`][] of a concrete battery class instead.

        It is only provided for using with a newer version of the API where
        the client doesn't know about the new battery type yet (i.e. for use
        with [`UnrecognizedBattery`][...UnrecognizedBattery]).
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is Battery:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)

    @property
    @typing_extensions.deprecated(
        "BatteryType is deprecated; identify batteries via isinstance() on the "
        "class hierarchy, or convert with "
        "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
    )
    def type(self) -> BatteryType | int:
        """The deprecated type of this battery."""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            try:
                return BatteryType(self._type)
            except ValueError:
                return self._type


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnspecifiedBattery(Battery):
    """A battery of an unspecified type."""

    _type: int = dataclasses.field(default=0, repr=False)  # BatteryType.UNSPECIFIED
    """The type of this battery.

    Note:
        This should not be used normally, you should test if a battery
        [`isinstance`][] of a concrete battery class instead.

        It is only provided for using with a newer version of the API where
        the client doesn't know about the new battery type yet (i.e. for use
        with [`UnrecognizedBattery`][...UnrecognizedBattery]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class LiIonBattery(Battery):
    """A Li-ion battery."""

    _type: int = dataclasses.field(default=1, repr=False)  # BatteryType.LI_ION
    """The type of this battery.

    Note:
        This should not be used normally, you should test if a battery
        [`isinstance`][] of a concrete battery class instead.

        It is only provided for using with a newer version of the API where
        the client doesn't know about the new battery type yet (i.e. for use
        with [`UnrecognizedBattery`][...UnrecognizedBattery]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class NaIonBattery(Battery):
    """A Na-ion battery."""

    _type: int = dataclasses.field(default=2, repr=False)  # BatteryType.NA_ION
    """The type of this battery.

    Note:
        This should not be used normally, you should test if a battery
        [`isinstance`][] of a concrete battery class instead.

        It is only provided for using with a newer version of the API where
        the client doesn't know about the new battery type yet (i.e. for use
        with [`UnrecognizedBattery`][...UnrecognizedBattery]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedBattery(Battery):
    """A battery of an unrecognized type."""

    _type: int = dataclasses.field(repr=False)
    """The unrecognized type of this battery."""

    @property
    @typing_extensions.override
    def type(self) -> int:
        """The deprecated type of this battery."""
        return self._type


BatteryTypes: TypeAlias = (
    LiIonBattery | NaIonBattery | UnrecognizedBattery | UnspecifiedBattery
)
"""All possible battery types."""
