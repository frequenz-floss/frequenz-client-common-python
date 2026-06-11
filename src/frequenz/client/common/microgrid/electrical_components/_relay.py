# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Relay electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Relay(ElectricalComponent):
    """A relay electrical component."""

    category: Literal[ComponentCategory.RELAY] = ComponentCategory.RELAY
    """The category of this electrical component."""
