# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""CHP electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Chp(ElectricalComponent):
    """A combined heat and power (CHP) electrical component."""

    category: Literal[ComponentCategory.CHP] = ComponentCategory.CHP
    """The category of this electrical component."""
