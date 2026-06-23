# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""PLC electrical component."""

import dataclasses
from typing import Literal

from ._category import ElectricalComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Plc(ElectricalComponent):
    """A programmable logic controller (PLC) electrical component."""

    category: Literal[ElectricalComponentCategory.PLC] = ElectricalComponentCategory.PLC
    """The category of this electrical component."""
