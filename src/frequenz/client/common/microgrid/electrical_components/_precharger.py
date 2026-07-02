# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Precharger electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class Precharger(ElectricalComponent):
    """A precharger electrical component."""

    _category: int = dataclasses.field(
        default=8, repr=False
    )  # ElectricalComponentCategory.PRECHARGER
    """The category of this electrical component."""
