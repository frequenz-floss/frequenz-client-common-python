# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Module to define the microgrid used with the common client."""

from __future__ import annotations  # required for constructor type hinting

from dataclasses import dataclass
from typing import List, Self

# pylint: disable=import-error, no-name-in-module
from frequenz.api.common.v1.microgrid.microgrid_pb2 import (
    MicrogridComponentIDs as PBMicrogridComponentIDs,
)


@dataclass(frozen=True, kw_only=True)
class MicrogridComponentIDs:
    """Linking component IDs with their respective microgrid ID."""

    microgrid_id: int
    """The ID of the microgrid."""

    component_ids: List[int]
    """List of component IDs belonging to this microgrid."""

    @classmethod
    def from_proto(cls, microgrid_component_ids: PBMicrogridComponentIDs) -> Self:
        """Convert a protobuf MicrogridComponentIDs to MicrogridComponentIDs object.

        Args:
            microgrid_component_ids: MicrogridComponentIDs to convert.

        Returns:
            MicrogridComponentIDs object corresponding to the protobuf message.
        """
        return cls(
            microgrid_id=microgrid_component_ids.microgrid_id,
            component_ids=List(microgrid_component_ids.component_ids),
        )

    def to_proto(self) -> PBMicrogridComponentIDs:
        """Convert a MicrogridComponentIDs object to protobuf MicrogridComponentIDs.

        Returns:
            Protobuf message corresponding to the MicrogridComponentIDs object.
        """
        return PBMicrogridComponentIDs(
            microgrid_id=self.microgrid_id,
            component_ids=List(self.component_ids),
        )
