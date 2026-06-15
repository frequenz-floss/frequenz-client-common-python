# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Power transformer electrical component."""

import dataclasses
from typing import Literal

from ._category import ElectricalComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class PowerTransformer(ElectricalComponent):
    """A power transformer electrical component.

    Power transformers are used to step up or step down the voltage, keeping
    the power somewhat constant by increasing or decreasing the current.

    If voltage is stepped up, current is stepped down, and vice versa.

    Note:
        Power transformers have efficiency losses, so the output power is always less
        than the input power.
    """

    category: Literal[ElectricalComponentCategory.POWER_TRANSFORMER] = (
        ElectricalComponentCategory.POWER_TRANSFORMER
    )
    """The category of this electrical component."""

    primary_voltage: float
    """The primary voltage of the transformer, in volts.

    This is the input voltage that is stepped up or down.
    """

    secondary_voltage: float
    """The secondary voltage of the transformer, in volts.

    This is the output voltage that is the result of stepping the primary
    voltage up or down.
    """
