# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""HVAC electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Hvac(ElectricalComponent):
    """A heating, ventilation, and air conditioning (HVAC) electrical component."""

    category: Literal[ComponentCategory.HVAC] = ComponentCategory.HVAC
    """The category of this electrical component."""
