# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Meter electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Meter(ElectricalComponent):
    """A measuring meter electrical component."""

    category: Literal[ComponentCategory.METER] = ComponentCategory.METER
    """The category of this electrical component."""
