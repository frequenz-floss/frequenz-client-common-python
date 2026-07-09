# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Definition of a microgrid."""

import datetime
from dataclasses import dataclass, field
from typing import assert_never

from .._exception import UnrecognizedEnumValueError, UnspecifiedEnumValueError
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

    name: str
    """The name of the microgrid."""

    delivery_area: DeliveryArea | None
    """The delivery area where the microgrid is located, as identified by a specific code."""

    location: Location | None
    """The physical location of the microgrid, in geographical co-ordinates."""

    create_time: datetime.datetime
    """The UTC timestamp indicating when the microgrid was initially created."""

    _active: bool | int
    """Whether the microgrid is active.

    This stores the low-level representation of the microgrid state. It holds a `bool`
    for a known active/inactive status, the raw `int` `0` when the status is
    unspecified, or any other raw `int` not yet known to this client. Users should use
    [`Microgrid.is_active()`][.is_active] to obtain a clear boolean or a clear error.
    """

    _allow_construction: bool = field(
        default=False, repr=False, compare=False, hash=False
    )
    """Internal guard allowing construction only via the `microgrid_from_proto` converter."""

    def __post_init__(self) -> None:
        """Reject direct construction of this read-only type.

        Raises:
            TypeError: If the instance was not created via the
                [`microgrid_from_proto`][...proto.v1alpha8.microgrid_from_proto]
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
            UnspecifiedEnumValueError: If the status is unspecified.
            UnrecognizedEnumValueError: If the status is not recognized. The raw
                status value is available on the error's `value` attribute.
        """
        match self._active:
            case bool() as active:
                return active
            case 0:
                raise UnspecifiedEnumValueError(
                    f"status of microgrid {self} is unspecified"
                )
            case int() as value:
                raise UnrecognizedEnumValueError(
                    value, f"unrecognized status of microgrid {self}: {value!r}"
                )
            case unknown:
                assert_never(unknown)

    def __str__(self) -> str:
        """Return the ID of this microgrid as a string."""
        name = f":{self.name}" if self.name else ""
        return f"{self.id}{name}"
