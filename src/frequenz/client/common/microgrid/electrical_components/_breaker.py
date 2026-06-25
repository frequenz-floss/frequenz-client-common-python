# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Breaker electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Breaker(ElectricalComponent):
    """A breaker electrical component."""

    _category: int = dataclasses.field(
        default=7, repr=False
    )  # ElectricalComponentCategory.BREAKER
    """The category of this electrical component."""
