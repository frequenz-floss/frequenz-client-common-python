# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""UPS electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class UninterruptiblePowerSupply(ElectricalComponent):
    """An uninterruptible power supply (UPS) electrical component."""
