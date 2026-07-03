# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Capacitor bank electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class CapacitorBank(ElectricalComponent):
    """A capacitor bank electrical component."""
