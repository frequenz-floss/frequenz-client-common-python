# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""HVAC electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Hvac(ElectricalComponent):
    """A heating, ventilation, and air conditioning (HVAC) electrical component."""

    _category: int = dataclasses.field(
        default=12, repr=False
    )  # ElectricalComponentCategory.HVAC
    """The category of this electrical component."""
