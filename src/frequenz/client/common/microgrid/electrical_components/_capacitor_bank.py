# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Capacitor bank electrical component."""

import dataclasses
from typing import Literal

from ._category import ElectricalComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class CapacitorBank(ElectricalComponent):
    """A capacitor bank electrical component."""

    category: Literal[ElectricalComponentCategory.CAPACITOR_BANK] = (
        ElectricalComponentCategory.CAPACITOR_BANK
    )
    """The category of this electrical component."""
