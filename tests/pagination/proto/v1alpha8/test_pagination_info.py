# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for pagination info protobuf v1alpha8 conversions."""

from frequenz.api.common.v1alpha8.pagination import pagination_info_pb2

from frequenz.client.common.pagination import PaginationInfo
from frequenz.client.common.pagination.proto.v1alpha8 import (
    pagination_info_from_proto,
    pagination_info_to_proto,
)


def test_pagination_info_from_proto_with_token() -> None:
    """Test converting a protobuf PaginationInfo with a token."""
    proto = pagination_info_pb2.PaginationInfo(total_items=100, next_page_token="token")
    info = pagination_info_from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token == "token"


def test_pagination_info_from_proto_empty_token() -> None:
    """Test converting an empty protobuf token to None."""
    proto = pagination_info_pb2.PaginationInfo(total_items=100, next_page_token="")
    info = pagination_info_from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token is None


def test_pagination_info_to_proto_with_token() -> None:
    """Test converting a PaginationInfo with a token to protobuf."""
    info = PaginationInfo(total_items=100, next_page_token="token")
    proto = pagination_info_to_proto(info)
    assert proto.total_items == 100
    assert proto.next_page_token == "token"


def test_pagination_info_roundtrip() -> None:
    """Test round-tripping PaginationInfo to protobuf and back."""
    info = PaginationInfo(total_items=100, next_page_token="token")
    proto = pagination_info_to_proto(info)
    roundtripped_info = pagination_info_from_proto(proto)
    assert roundtripped_info == info
