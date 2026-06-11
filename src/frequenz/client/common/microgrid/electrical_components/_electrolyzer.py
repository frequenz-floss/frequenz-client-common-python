# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Electrolyzer electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Electrolyzer(ElectricalComponent):
    """An electrolyzer electrical component."""

    category: Literal[ComponentCategory.ELECTROLYZER] = ComponentCategory.ELECTROLYZER
    """The category of this electrical component."""
