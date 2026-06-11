# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Converter electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Converter(ElectricalComponent):
    """An AC-DC converter electrical component."""

    category: Literal[ComponentCategory.CONVERTER] = ComponentCategory.CONVERTER
    """The category of this electrical component."""
