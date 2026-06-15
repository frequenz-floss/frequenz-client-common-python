# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Electrical component operational modes."""

import enum


@enum.unique
class ElectricalComponentOperationalMode(enum.Enum):
    """The operational mode of an electrical component.

    This indicates whether the component is active and operational, and whether it
    provides telemetry data, accepts control commands, or both.
    """

    UNSPECIFIED = 0
    """Default value when the operational mode is not explicitly set."""

    INACTIVE = 1
    """The component is inactive and not operational.

    It does not provide telemetry data, and it does not accept control commands.
    """

    TELEMETRY_ONLY = 2
    """The component is active and operational, providing telemetry data only.

    It does not accept control commands.
    """

    CONTROL_ONLY = 3
    """The component is active and operational, accepting control commands only.

    It does not provide telemetry data.
    """

    CONTROL_AND_TELEMETRY = 4
    """The component is active and operational.

    It provides telemetry data and accepts control commands.
    """
