# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Precharger electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Precharger(ElectricalComponent):
    """A precharger electrical component."""

    category: Literal[ComponentCategory.PRECHARGER] = ComponentCategory.PRECHARGER
    """The category of this electrical component."""
