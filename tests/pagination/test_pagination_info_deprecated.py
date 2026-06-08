# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Tests for the pagination module."""

import pytest
from frequenz.api.common.v1.pagination.pagination_info_pb2 import (
    PaginationInfo as PBPaginationInfo,
)
from frequenz.api.common.v1alpha8.pagination.pagination_info_pb2 import (
    PaginationInfo as PBPaginationInfoAlpha8,
)

from frequenz.client.common.pagination import Info, PaginationInfo


def test_pagination_info_from_proto_v1() -> None:
    """Test the PaginationInfo from_proto method with v1 proto."""
    proto = PBPaginationInfo(total_items=100, next_page_token="token")
    with pytest.deprecated_call():
        info = PaginationInfo.from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token == "token"


def test_pagination_info_from_proto_v1alpha8() -> None:
    """Test the PaginationInfo from_proto method with v1alpha8 proto."""
    proto = PBPaginationInfoAlpha8(total_items=100, next_page_token="token")
    with pytest.deprecated_call():
        info = PaginationInfo.from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token == "token"


def test_pagination_info_from_proto_v1_no_token() -> None:
    """Test the PaginationInfo from_proto method with v1 proto and no token."""
    proto = PBPaginationInfo(total_items=100)
    with pytest.deprecated_call():
        info = PaginationInfo.from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token is None


def test_pagination_info_from_proto_v1alpha8_no_token() -> None:
    """Test the PaginationInfo from_proto method with v1alpha8 proto and no token."""
    proto = PBPaginationInfoAlpha8(total_items=100)
    with pytest.deprecated_call():
        info = PaginationInfo.from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token is None


def test_pagination_info_from_proto_v1_empty_token() -> None:
    """Test the PaginationInfo from_proto method with v1 proto and an empty token."""
    proto = PBPaginationInfo(total_items=100, next_page_token="")
    with pytest.deprecated_call():
        info = PaginationInfo.from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token is None


def test_pagination_info_from_proto_v1alpha8_empty_token() -> None:
    """Test the PaginationInfo from_proto method with v1alpha8 proto and an empty token."""
    proto = PBPaginationInfoAlpha8(total_items=100, next_page_token="")
    with pytest.deprecated_call():
        info = PaginationInfo.from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token is None


def test_pagination_info_to_proto_v1() -> None:
    """Test the PaginationInfo to_proto method."""
    info = PaginationInfo(total_items=100, next_page_token="token")
    with pytest.deprecated_call():
        proto = info.to_proto()
    assert proto.total_items == 100
    assert proto.next_page_token == "token"


def test_pagination_info_to_proto_v1alpha8() -> None:
    """Test the PaginationInfo to_proto_v1alpha8 method."""
    info = PaginationInfo(total_items=100, next_page_token="token")
    with pytest.deprecated_call():
        proto = info.to_proto_v1alpha8()
    assert proto.total_items == 100
    assert proto.next_page_token == "token"


def test_deprecated_info_from_proto() -> None:
    """Test the deprecated Info from_proto method."""
    proto = PBPaginationInfo(total_items=100, next_page_token="token")
    with pytest.deprecated_call():
        info = Info.from_proto(proto)
    assert info.total_items == 100
    assert info.next_page_token == "token"


def test_deprecated_info_to_proto() -> None:
    """Test the deprecated Info to_proto method."""
    with pytest.deprecated_call():
        info = Info(total_items=100, next_page_token="token")
    proto = info.to_proto()
    assert proto.total_items == 100
    assert proto.next_page_token == "token"
