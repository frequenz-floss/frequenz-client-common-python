# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Module to define the pagination information used with the common client."""

from __future__ import annotations  # required for constructor type hinting

from dataclasses import dataclass
from typing import Self

# pylint: disable=no-name-in-module
from frequenz.api.common.v1.pagination.pagination_info_pb2 import (
    PaginationInfo as PBPaginationInfo,
)
from frequenz.api.common.v1alpha8.pagination.pagination_info_pb2 import (
    PaginationInfo as PBPaginationInfoAlpha8,
)

# pylint: enable=no-name-in-module


@dataclass(frozen=True, kw_only=True)
class PaginationInfo:
    """Information about the pagination of a list request."""

    total_items: int
    """The total number of items that match the request."""

    next_page_token: str | None = None
    """The token identifying the next page of results."""

    @classmethod
    def from_proto(
        cls, pagination_info: PBPaginationInfoAlpha8 | PBPaginationInfo
    ) -> Self:
        """Convert a protobuf PBPaginationInfo to Info object.

        Args:
            pagination_info: Info to convert.
        Returns:
            Info object corresponding to the protobuf message.
        """
        # We check for truthiness here to handle both cases where the token is
        # not set (defaults to "") or is explicitly set to "". In both
        # situations, we want to return `None`. Using `HasField("next_page_token")`
        # would not handle the case where the token is explicitly set to "".
        return cls(
            total_items=pagination_info.total_items,
            next_page_token=(
                pagination_info.next_page_token if pagination_info.next_page_token else None
            ),
        )

    def to_proto_v1alpha8(self) -> PBPaginationInfoAlpha8:
        """Convert a Info object to protobuf PBPaginationInfo.

        Returns:
            Protobuf message corresponding to the Info object.
        """
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from frequenz.client.common.pagination.proto.v1alpha8 import (
            pagination_info_to_proto,
        )

        return pagination_info_to_proto(self)

    def to_proto(self) -> PBPaginationInfo:
        """Convert a Info object to protobuf PBPaginationInfo.

        Returns:
            Protobuf message corresponding to the Info object.
        """
        return PBPaginationInfo(
            total_items=self.total_items,
            next_page_token=self.next_page_token,
        )
