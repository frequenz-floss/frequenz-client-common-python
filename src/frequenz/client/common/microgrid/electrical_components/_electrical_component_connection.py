# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Electrical component connection."""

import dataclasses
from datetime import datetime, timezone
from typing import Any, Self, assert_never

from .._lifetime import InvalidLifetime, InvalidLifetimeError, Lifetime
from ._ids import ElectricalComponentId


@dataclasses.dataclass(frozen=True, kw_only=True)
class BaseElectricalComponentConnection:
    """A base class for all electrical component connections.

    This is the common supertype of every kind of connection, both
    well-formed (see
    [`ElectricalComponentConnection`][..ElectricalComponentConnection]) and
    problematic (see
    [`ProblematicElectricalComponentConnection`][..ProblematicElectricalComponentConnection]).
    It cannot be instantiated directly; use one of its concrete subclasses
    instead, or obtain instances via the corresponding `*_from_proto`
    converter.

    Note: Physical Representation
        This object is not about data flow but rather about the physical
        electrical connections between electrical components. Therefore, the IDs for the
        source and destination electrical components correspond to the actual setup within
        the microgrid.

    Note: Direction
        The direction of the connection follows the flow of current away from the
        grid connection point, or in case of islands, away from the islanding
        point. This direction is aligned with positive current according to the
        [Passive Sign Convention](https://en.wikipedia.org/wiki/Passive_sign_convention).

    Note: Historical Data
        The timestamps of when a connection was created and terminated allow for
        tracking the changes over time to a microgrid, providing insights into
        when and how the microgrid infrastructure has been modified.
    """

    source_id: ElectricalComponentId
    """The unique identifier of the electrical component where the connection originates.

    This is aligned with the direction of current flow away from the grid connection
    point, or in case of islands, away from the islanding point.
    """

    destination_id: ElectricalComponentId
    """The unique ID of the electrical component where the connection terminates.

    This is the electrical component towards which the current flows.
    """

    operational_lifetime: Lifetime | InvalidLifetime = dataclasses.field(
        default_factory=Lifetime
    )
    """The operational lifetime of the connection.

    An [`InvalidLifetime`][....InvalidLifetime] preserves malformed wire data.

    Tip:
        Prefer [`get_operational_lifetime()`][..get_operational_lifetime] when
        a valid lifetime is required.
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is BaseElectricalComponentConnection:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)

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
        """Check whether this connection is operational at a specific timestamp.

        Args:
            timestamp: The timestamp to check against the operational lifetime.

        Returns:
            Whether this connection is operational at the given timestamp.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        return self.get_operational_lifetime().is_operational_at(timestamp)

    def is_operational_now(self) -> bool:  # noqa: DOC502
        """Whether this connection is currently operational.

        Returns:
            Whether this connection is operational at the current time.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        return self.is_operational_at(datetime.now(timezone.utc))

    def __str__(self) -> str:
        """Return a human-readable string representation of this instance."""
        return f"{self.source_id}->{self.destination_id}"


@dataclasses.dataclass(frozen=True, kw_only=True)
class ElectricalComponentConnection(BaseElectricalComponentConnection):
    """A single electrical link between two distinct electrical components in a microgrid.

    This is the well-formed case of an electrical component connection: the
    source and destination are guaranteed to be different components.
    Malformed cases (e.g. self-loops) are represented by dedicated
    subclasses of
    [`ProblematicElectricalComponentConnection`][..ProblematicElectricalComponentConnection]
    instead.
    """

    def __post_init__(self) -> None:
        """Ensure that the source and destination electrical components are different.

        Raises:
            ValueError: If
                [`source_id`][...BaseElectricalComponentConnection.source_id]
                and
                [`destination_id`][...BaseElectricalComponentConnection.destination_id]
                are equal, since that would describe a self-loop rather than
                a well-formed connection.
        """
        if self.source_id == self.destination_id:
            raise ValueError("Source and destination components must be different")
