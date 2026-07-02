# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Problematic electrical components."""

import dataclasses
from typing import Any, Self

from typing_extensions import override

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class ProblematicElectricalComponent(ElectricalComponent):
    """An abstract electrical component with a problem."""

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is ProblematicElectricalComponent:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnspecifiedElectricalComponent(ProblematicElectricalComponent):
    """An electrical component of unspecified type."""

    _category: int = dataclasses.field(
        default=0, repr=False
    )  # ElectricalComponentCategory.UNSPECIFIED
    """The category of this electrical component."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedElectricalComponent(ProblematicElectricalComponent):
    """An electrical component of an unrecognized type.

    This is used for components whose category is not known to this version of
    the library.
    """

    _category: int = dataclasses.field(repr=False)
    """The category of this electrical component."""

    @property
    @override
    def category(self) -> int:
        """The deprecated category of this electrical component."""
        return self._category


@dataclasses.dataclass(frozen=True, kw_only=True)
class MismatchedCategoryElectricalComponent(ProblematicElectricalComponent):
    """An electrical component with a mismatch in the category.

    This electrical component declared a category but carries category specific
    metadata that doesn't match the declared category.
    """

    _category: int = dataclasses.field(repr=False)
    """The category of this electrical component."""

    @property
    @override
    def category(self) -> int:
        """The deprecated category of this electrical component."""
        return self._category
