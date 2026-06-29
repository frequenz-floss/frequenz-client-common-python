# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Definition of a microgrid."""

import datetime
from dataclasses import dataclass, field

from .._exception import UnspecifiedValueError
from ..grid._delivery_area import DeliveryArea
from ..types._location import Location
from ._ids import EnterpriseId, MicrogridId


@dataclass(frozen=True, kw_only=True)
class Microgrid:  # pylint: disable=too-many-instance-attributes
    """A localized grouping of electricity generation, energy storage, and loads.

    A microgrid is a localized grouping of electricity generation, energy storage, and
    loads that normally operates connected to a traditional centralized grid.

    Each microgrid has a unique identifier and is associated with an enterprise account.

    A key feature is that it has a physical location and is situated in a delivery area.

    Note: Key Concepts
        - Physical Location: Geographical coordinates specify the exact physical
          location of the microgrid.
        - Delivery Area: Each microgrid is part of a broader delivery area, which is
          crucial for energy trading and compliance.
    """

    id: MicrogridId
    """The unique identifier of the microgrid."""

    enterprise_id: EnterpriseId
    """The unique identifier linking this microgrid to its parent enterprise account."""

    name: str | None
    """The name of the microgrid."""

    delivery_area: DeliveryArea | None
    """The delivery area where the microgrid is located, as identified by a specific code."""

    location: Location | None
    """The physical location of the microgrid, in geographical co-ordinates."""

    create_time: datetime.datetime
    """The UTC timestamp indicating when the microgrid was initially created."""

    _active: bool | None
    """Whether the microgrid is active, or `None` if its status is unspecified."""

    _allow_construction: bool = field(
        default=False, repr=False, compare=False, hash=False
    )
    """Internal guard allowing construction only via the `microgrid_from_proto` converter."""

    def __post_init__(self) -> None:
        """Reject direct construction of this read-only type.

        Raises:
            TypeError: If the instance was not created via the `microgrid_from_proto`
                converter.
        """
        if not self._allow_construction:
            raise TypeError(
                f"{type(self).__name__} cannot be constructed directly; obtain "
                "instances via the microgrid_from_proto converter."
            )

    def is_active(self) -> bool:
        """Return whether the microgrid is active.

        Returns:
            Whether the microgrid is active.

        Raises:
            UnspecifiedValueError: If the status is unspecified, so whether the
                microgrid is active is unknown.
        """
        if self._active is None:
            raise UnspecifiedValueError(
                f"status of microgrid {self} is unspecified; active state is unknown"
            )
        return self._active

    def __str__(self) -> str:
        """Return the ID of this microgrid as a string."""
        name = f":{self.name}" if self.name else ""
        return f"{self.id}{name}"
