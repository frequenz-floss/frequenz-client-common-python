# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Converter electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Converter(ElectricalComponent):
    """An AC-DC converter electrical component."""
