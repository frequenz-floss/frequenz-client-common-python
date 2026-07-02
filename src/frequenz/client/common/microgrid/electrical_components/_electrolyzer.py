# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Electrolyzer electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Electrolyzer(ElectricalComponent):
    """An electrolyzer electrical component."""

    _category: int = dataclasses.field(
        default=10, repr=False
    )  # ElectricalComponentCategory.ELECTROLYZER
    """The category of this electrical component."""
