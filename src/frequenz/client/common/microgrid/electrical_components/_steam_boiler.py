# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Steam boiler electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class SteamBoiler(ElectricalComponent):
    """A steam boiler electrical component."""

    category: Literal[ComponentCategory.STEAM_BOILER] = ComponentCategory.STEAM_BOILER
    """The category of this electrical component."""
