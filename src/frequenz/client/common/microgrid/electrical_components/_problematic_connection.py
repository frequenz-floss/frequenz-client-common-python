# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Problematic electrical component connections."""

import dataclasses
from typing import Any, Self

from ._electrical_component_connection import BaseElectricalComponentConnection


@dataclasses.dataclass(frozen=True, kw_only=True)
class ProblematicElectricalComponentConnection(BaseElectricalComponentConnection):
    """An abstract electrical component connection with a problem.

    This is the base class for connections that carry a data-integrity issue.

    Problematic connections are siblings of the well-formed
    [`ElectricalComponentConnection`][..ElectricalComponentConnection]: both
    extend
    [`BaseElectricalComponentConnection`][..BaseElectricalComponentConnection].
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is ProblematicElectricalComponentConnection:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclasses.dataclass(frozen=True, kw_only=True)
class SelfReferencingElectricalComponentConnection(
    ProblematicElectricalComponentConnection
):
    """An electrical component connection whose source and destination are the same.

    This represents a self-loop in the microgrid topology, which is physically
    impossible and normally invalid. Instances of this class are produced by
    the ``*_from_proto`` converters when they receive a connection whose
    source and destination component IDs are identical, so that the
    problematic data is exposed to the caller instead of being silently
    discarded.
    """

    def __post_init__(self) -> None:
        """Ensure that source and destination refer to the same component.

        Raises:
            ValueError: If
                [`source_id`][...BaseElectricalComponentConnection.source_id]
                and
                [`destination_id`][...BaseElectricalComponentConnection.destination_id]
                are different, since a self-referencing connection is defined
                by them being the same.
        """
        if self.source_id != self.destination_id:
            raise ValueError(
                "Source and destination components must be the same for a "
                "self-referencing electrical component connection"
            )
