# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Definition of a microgrid sensor."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import assert_never

from .._ids import MicrogridId
from .._lifetime import InvalidLifetime, InvalidLifetimeError, Lifetime
from ._id import SensorId


@dataclass(frozen=True, kw_only=True)
class Sensor:
    """A sensor that measures a physical metric in the microgrid's surroundings.

    Sensors are not part of the electrical infrastructure but provide
    environmental data such as temperature, humidity, and solar irradiance.
    """

    id: SensorId
    """The unique identifier of the sensor."""

    microgrid_id: MicrogridId
    """The unique identifier of the parent microgrid."""

    name: str
    """The name of the sensor.

    An empty string when the wire did not set it.
    """

    model: str
    """The model of the sensor.

    This includes both the manufacturer and the model name.
    """

    operational_lifetime: Lifetime | InvalidLifetime = field(default_factory=Lifetime)
    """The operational lifetime of the sensor.

    An [`InvalidLifetime`][....InvalidLifetime] preserves malformed wire data.

    Tip:
        Prefer [`get_operational_lifetime()`][..get_operational_lifetime] when
        a valid lifetime is required.
    """

    _allow_construction: bool = field(
        default=False, repr=False, compare=False, hash=False
    )
    """Internal guard allowing construction only via the `sensor_from_proto` converter."""

    def __post_init__(self) -> None:
        """Reject direct construction of this read-only type.

        Raises:
            TypeError: If the instance was not created via the
                [`sensor_from_proto`][...proto.v1alpha8.sensor_from_proto]
                converter.
        """
        if not self._allow_construction:
            raise TypeError(
                f"{type(self).__name__} cannot be constructed directly; obtain "
                "instances via the sensor_from_proto converter."
            )

    def get_operational_lifetime(self) -> Lifetime:
        """Return the operational lifetime as a valid `Lifetime`.

        Returns:
            The valid operational lifetime.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        match self.operational_lifetime:
            case InvalidLifetime() as invalid:
                raise InvalidLifetimeError(self, "operational_lifetime", invalid)
            case Lifetime() as valid:
                return valid
            case unknown:
                assert_never(unknown)

    def is_operational_at(self, timestamp: datetime) -> bool:  # noqa: DOC502
        """Check whether this sensor is operational at a specific timestamp.

        Args:
            timestamp: The timestamp to check.

        Returns:
            Whether this sensor is operational at the given timestamp.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        return self.get_operational_lifetime().is_operational_at(timestamp)

    def is_operational_now(self) -> bool:  # noqa: DOC502
        """Check whether this sensor is currently operational.

        Returns:
            Whether this sensor is operational at the current time.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        return self.is_operational_at(datetime.now(timezone.utc))

    @property
    def identity(self) -> tuple[SensorId, MicrogridId]:
        """The identity of this sensor.

        This uses the sensor ID and microgrid ID to identify a sensor without
        considering the other attributes, so even if a sensor state changed, the
        identity remains the same.
        """
        return (self.id, self.microgrid_id)

    def __str__(self) -> str:
        """Return the ID of this sensor as a string, followed by its name if any."""
        name = f":{self.name}" if self.name else ""
        return f"{self.id}{name}"
