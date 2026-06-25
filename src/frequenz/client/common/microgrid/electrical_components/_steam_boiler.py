# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Steam boiler electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class SteamBoiler(ElectricalComponent):
    """A steam boiler electrical component."""

    _category: int = dataclasses.field(
        default=19, repr=False
    )  # ElectricalComponentCategory.STEAM_BOILER
    """The category of this electrical component."""
