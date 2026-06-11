# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Base electrical component from which all other electrical components inherit."""

import dataclasses
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self

from frequenz.client.common.microgrid import MicrogridId

from ...metrics import Bounds, Metric
from ...types import Lifetime
from ._category import ElectricalComponentCategory
from ._ids import ElectricalComponentId


@dataclasses.dataclass(frozen=True, kw_only=True)
class ElectricalComponent:  # pylint: disable=too-many-instance-attributes
    """A base class for all electrical components."""

    id: ElectricalComponentId
    """This electrical component's ID."""

    microgrid_id: MicrogridId
    """The ID of the microgrid this electrical component belongs to."""

    category: ElectricalComponentCategory | int
    """The category of this electrical component.

    Note:
        This should not be used normally, you should test if an electrical component
        [`isinstance`][] of a concrete electrical component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about a new category yet (i.e. for use with
        [`UnrecognizedComponent`][...UnrecognizedComponent]) and in case some low level
        code needs to know the category of an electrical component.
        """

    name: str | None = None
    """The name of this electrical component."""

    manufacturer: str | None = None
    """The manufacturer of this electrical component."""

    model_name: str | None = None
    """The model name of this electrical component."""

    operational_lifetime: Lifetime = dataclasses.field(default_factory=Lifetime)
    """The operational lifetime of this electrical component."""

    rated_bounds: Mapping[Metric | int, Bounds] = dataclasses.field(
        default_factory=dict,
        # dict is not hashable, so we don't use this field to calculate the hash. This
        # shouldn't be a problem since it is very unlikely that two components with all
        # other attributes being equal would have different category specific metadata,
        # so hash collisions should be still very unlikely.
        hash=False,
    )
    """List of rated bounds present for the electrical component identified by Metric."""

    category_specific_metadata: Mapping[str, Any] = dataclasses.field(
        default_factory=dict,
        # dict is not hashable, so we don't use this field to calculate the hash. This
        # shouldn't be a problem since it is very unlikely that two components with all
        # other attributes being equal would have different category specific metadata,
        # so hash collisions should be still very unlikely.
        hash=False,
    )
    """The category specific metadata of this electrical component.

    Note:
        This should not be used normally, it is only useful when accessing a newer
        version of the API where the client doesn't know about the new metadata fields
        yet (i.e. for use with [`UnrecognizedComponent`][...UnrecognizedComponent]).
    """

    def __new__(cls, *_: Any, **__: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is ElectricalComponent:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)

    def is_operational_at(self, timestamp: datetime) -> bool:
        """Check whether this electrical component is operational at a specific timestamp.

        Args:
            timestamp: The timestamp to check.

        Returns:
            Whether this electrical component is operational at the given timestamp.
        """
        return self.operational_lifetime.is_operational_at(timestamp)

    def is_operational_now(self) -> bool:
        """Check whether this electrical component is currently operational.

        Returns:
            Whether this electrical component is operational at the current time.
        """
        return self.is_operational_at(datetime.now(timezone.utc))

    @property
    def identity(self) -> tuple[ElectricalComponentId, MicrogridId]:
        """The identity of this electrical component.

        This uses the component ID and microgrid ID to identify an electrical
        component without considering the other attributes, so even if an electrical
        component state changed, the identity remains the same.
        """
        return (self.id, self.microgrid_id)

    def __str__(self) -> str:
        """Return a human-readable string representation of this instance."""
        name = f":{self.name}" if self.name else ""
        return f"{self.id}<{type(self).__name__}>{name}"
