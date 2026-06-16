# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Problematic electrical components."""

import dataclasses
from typing import Any, Literal, Self

from ._category import ElectricalComponentCategory
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

    category: Literal[ElectricalComponentCategory.UNSPECIFIED] = (
        ElectricalComponentCategory.UNSPECIFIED
    )
    """The category of this electrical component."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class UnrecognizedElectricalComponent(ProblematicElectricalComponent):
    """An electrical component of an unrecognized type."""

    category: int
    """The category of this electrical component."""


@dataclasses.dataclass(frozen=True, kw_only=True)
class MismatchedCategoryElectricalComponent(ProblematicElectricalComponent):
    """An electrical component with a mismatch in the category.

    This electrical component declared a category but carries category specific
    metadata that doesn't match the declared category.
    """

    category: ElectricalComponentCategory | int
    """The category of this electrical component."""
