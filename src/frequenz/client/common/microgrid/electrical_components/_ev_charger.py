# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Electric vehicle (EV) charger electrical component."""

import dataclasses
import warnings
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

    _category: int = dataclasses.field(
        default=6, repr=False
    )  # ElectricalComponentCategory.EV_CHARGER
    """The category of this electrical component.

    Note:
        This should not be used normally, you should test if an electrical component
        [`isinstance`][] of a concrete EV charger class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about a new category yet (i.e. for use with
        [`UnrecognizedElectricalComponent`][...UnrecognizedElectricalComponent]) and in
        case some low level code needs to know the category of an electrical component.
    """

    _type: int = dataclasses.field(repr=False)
    """The type of this EV charger.

    Note:
        This should not be used normally, you should test if an EV charger
        [`isinstance`][] of a concrete component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new EV charger type yet (i.e. for use with
        [`UnrecognizedEvCharger`][...UnrecognizedEvCharger]).
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is EvCharger:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)

    @property
    @typing_extensions.deprecated(
        "EvChargerType is deprecated; identify EV chargers via isinstance() on the "
        "class hierarchy, or convert with "
        "electrical_component_class_to_proto()/electrical_component_class_from_proto()."
    )
    def type(self) -> EvChargerType | int:
        """The deprecated type of this EV charger."""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            try:
                return EvChargerType(self._type)
            except ValueError:
                return self._type


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnspecifiedEvCharger(EvCharger):
    """An EV charger of an unspecified type."""

    _type: int = dataclasses.field(default=0, repr=False)  # EvChargerType.UNSPECIFIED
    """The type of this EV charger.

    Note:
        This should not be used normally, you should test if an EV charger
        [`isinstance`][] of a concrete component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new EV charger type yet (i.e. for use with
        [`UnrecognizedEvCharger`][...UnrecognizedEvCharger]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class AcEvCharger(EvCharger):
    """An EV charger that supports AC charging only."""

    _type: int = dataclasses.field(default=1, repr=False)  # EvChargerType.AC
    """The type of this EV charger.

    Note:
        This should not be used normally, you should test if an EV charger
        [`isinstance`][] of a concrete component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new EV charger type yet (i.e. for use with
        [`UnrecognizedEvCharger`][...UnrecognizedEvCharger]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class DcEvCharger(EvCharger):
    """An EV charger that supports DC charging only."""

    _type: int = dataclasses.field(default=2, repr=False)  # EvChargerType.DC
    """The type of this EV charger.

    Note:
        This should not be used normally, you should test if an EV charger
        [`isinstance`][] of a concrete component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new EV charger type yet (i.e. for use with
        [`UnrecognizedEvCharger`][...UnrecognizedEvCharger]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class HybridEvCharger(EvCharger):
    """An EV charger that supports both AC and DC charging."""

    _type: int = dataclasses.field(default=3, repr=False)  # EvChargerType.HYBRID
    """The type of this EV charger.

    Note:
        This should not be used normally, you should test if an EV charger
        [`isinstance`][] of a concrete component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about the new EV charger type yet (i.e. for use with
        [`UnrecognizedEvCharger`][...UnrecognizedEvCharger]).
    """


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedEvCharger(EvCharger):
    """An EV charger of an unrecognized type."""

    _type: int = dataclasses.field(repr=False)
    """The unrecognized type of this EV charger."""

    @property
    @typing_extensions.override
    def type(self) -> int:
        """The deprecated type of this EV charger."""
        return self._type


EvChargerTypes: TypeAlias = (
    UnspecifiedEvCharger
    | AcEvCharger
    | DcEvCharger
    | HybridEvCharger
    | UnrecognizedEvCharger
)
"""All possible EV charger types."""
