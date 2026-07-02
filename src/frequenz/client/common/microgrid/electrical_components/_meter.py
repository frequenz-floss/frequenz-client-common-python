# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Meter electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Meter(ElectricalComponent):
    """A measuring meter electrical component."""

    _category: int = dataclasses.field(
        default=2, repr=False
    )  # ElectricalComponentCategory.METER
    """The category of this electrical component."""
