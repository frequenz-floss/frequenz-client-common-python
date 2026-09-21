# License: MIT
# Copyright © 2022 Frequenz Energy-as-a-Service GmbH

"""Electrical component identifier."""

from typing import final

from frequenz.core.id import BaseId


@final
class ElectricalComponentId(BaseId, str_prefix="ECID"):
    """A unique identifier for a microgrid electrical component."""
