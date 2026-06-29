# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of PaginationInfo from/to protobuf v1alpha8."""

from frequenz.api.common.v1alpha8.pagination.pagination_info_pb2 import (
    PaginationInfo as PaginationInfoPb,
)

from ....pagination import PaginationInfo


def pagination_info_from_proto(message: PaginationInfoPb) -> PaginationInfo:
    """Convert a protobuf message to a [`PaginationInfo`][....PaginationInfo] object.

    Args:
        message: The protobuf message to convert.

    Returns:
        The corresponding [`PaginationInfo`][....PaginationInfo] object.
    """
    return PaginationInfo(
        total_items=message.total_items,
        next_page_token=message.next_page_token if message.next_page_token else None,
    )


def pagination_info_to_proto(info: PaginationInfo) -> PaginationInfoPb:
    """Convert a [`PaginationInfo`][....PaginationInfo] object to a protobuf message.

    Args:
        info: The [`PaginationInfo`][....PaginationInfo] object to convert.

    Returns:
        The corresponding protobuf message.
    """
    return PaginationInfoPb(
        total_items=info.total_items,
        next_page_token=info.next_page_token,
    )
