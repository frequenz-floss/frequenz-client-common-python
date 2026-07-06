# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Electrolyzer electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Electrolyzer(ElectricalComponent):
    """An electrolyzer electrical component."""
