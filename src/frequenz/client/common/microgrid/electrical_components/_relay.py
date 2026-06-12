# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Relay electrical component."""

import dataclasses
from typing import Literal

from ._category import ElectricalComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Relay(ElectricalComponent):
    """A relay electrical component."""

    category: Literal[ElectricalComponentCategory.BREAKER] = (
        ElectricalComponentCategory.BREAKER
    )
    """The category of this electrical component."""
