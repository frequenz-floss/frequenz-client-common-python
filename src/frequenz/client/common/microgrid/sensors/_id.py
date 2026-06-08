# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Microgrid sensor identifiers."""

from typing import final

from frequenz.core.id import BaseId


@final
class SensorId(BaseId, str_prefix="SID"):
    """A unique identifier for a microgrid sensor."""
