# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Static transfer switch electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class StaticTransferSwitch(ElectricalComponent):
    """A static transfer switch electrical component."""
