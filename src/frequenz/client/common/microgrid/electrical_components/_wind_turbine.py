# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Wind turbine electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class WindTurbine(ElectricalComponent):
    """A wind turbine electrical component."""

    _category: int = dataclasses.field(
        default=18, repr=False
    )  # ElectricalComponentCategory.WIND_TURBINE
    """The category of this electrical component."""
