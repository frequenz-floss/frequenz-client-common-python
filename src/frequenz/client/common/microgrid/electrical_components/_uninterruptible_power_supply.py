# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""UPS electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class UninterruptiblePowerSupply(ElectricalComponent):
    """An uninterruptible power supply (UPS) electrical component."""

    _category: int = dataclasses.field(
        default=16, repr=False
    )  # ElectricalComponentCategory.UNINTERRUPTIBLE_POWER_SUPPLY
    """The category of this electrical component."""
