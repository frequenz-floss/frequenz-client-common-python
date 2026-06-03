# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Defines the electrical components that can be used in a microgrid."""

from typing import final

from frequenz.core.id import BaseId

from ._category import ElectricalComponentCategory
from ._diagnostic_code import ElectricalComponentDiagnosticCode
from ._state_code import ElectricalComponentStateCode


@final
class ElectricalComponentId(BaseId, str_prefix="CID"):
    """A unique identifier for a microgrid electrical component."""


__all__ = [
    "ElectricalComponentCategory",
    "ElectricalComponentDiagnosticCode",
    "ElectricalComponentId",
    "ElectricalComponentStateCode",
]
