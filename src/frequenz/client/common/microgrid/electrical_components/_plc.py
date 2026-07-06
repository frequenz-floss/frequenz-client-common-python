# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""PLC electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Plc(ElectricalComponent):
    """A programmable logic controller (PLC) electrical component."""
