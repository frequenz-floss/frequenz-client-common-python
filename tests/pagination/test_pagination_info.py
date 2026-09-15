# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for pagination info."""

import pytest

from frequenz.client.common.pagination import (
    BasePaginationInfo,
    InvalidPaginationInfo,
    PaginationInfo,
)


def test_base_cannot_be_instantiated_directly() -> None:
    """`BasePaginationInfo` refuses direct instantiation."""
    with pytest.raises(TypeError, match="Cannot instantiate BasePaginationInfo"):
        BasePaginationInfo(total_items=0)


def test_leaves_are_base_subclasses() -> None:
    """Both concrete types share the `BasePaginationInfo` supertype."""
    assert issubclass(PaginationInfo, BasePaginationInfo)
    assert issubclass(InvalidPaginationInfo, BasePaginationInfo)


def test_accepts_zero_total_items() -> None:
    """Zero total items should be accepted."""
    info = PaginationInfo(total_items=0)
    assert info.total_items == 0


def test_accepts_positive_total_items() -> None:
    """Positive total items should be accepted."""
    info = PaginationInfo(total_items=1)
    assert info.total_items == 1


def test_rejects_negative_total_items() -> None:
    """Negative total items should be rejected with the exact message."""
    with pytest.raises(
        ValueError,
        match=r"^total_items must be non-negative, not -1$",
    ):
        PaginationInfo(total_items=-1)


def test_token_defaults_to_none() -> None:
    """The next page token is optional."""
    assert PaginationInfo(total_items=0).next_page_token is None


@pytest.mark.parametrize(
    ("total_items", "next_page_token", "expected"),
    [
        (0, None, "items=0,next=None"),
        (100, "token", "items=100,next=token"),
    ],
)
def test_str(total_items: int, next_page_token: str | None, expected: str) -> None:
    """`PaginationInfo` renders compactly and without an invalid marker."""
    info = PaginationInfo(total_items=total_items, next_page_token=next_page_token)
    assert str(info) == expected


def test_invalid_accepts_negative_total_items() -> None:
    """`InvalidPaginationInfo` enforces no invariants on construction."""
    info = InvalidPaginationInfo(total_items=-1, next_page_token="token")
    assert info.total_items == -1
    assert info.next_page_token == "token"


@pytest.mark.parametrize(
    ("total_items", "next_page_token", "expected"),
    [
        (-1, None, "items=<invalid:-1>,next=None"),
        (-10, "token", "items=<invalid:-10>,next=token"),
        (0, None, "items=0,next=None"),
    ],
)
def test_invalid_str(
    total_items: int, next_page_token: str | None, expected: str
) -> None:
    """Only a negative count is marked as invalid."""
    info = InvalidPaginationInfo(
        total_items=total_items, next_page_token=next_page_token
    )
    assert str(info) == expected


def test_invalid_equality() -> None:
    """Two `InvalidPaginationInfo` instances with the same data are equal."""
    info1 = InvalidPaginationInfo(total_items=-1)
    info2 = InvalidPaginationInfo(total_items=-1)
    info3 = InvalidPaginationInfo(total_items=-2)
    assert info1 == info2
    assert info1 != info3


def test_valid_and_invalid_are_distinct() -> None:
    """A `PaginationInfo` and an `InvalidPaginationInfo` with same fields differ."""
    valid = PaginationInfo(total_items=1)
    invalid = InvalidPaginationInfo(total_items=1)
    assert valid != invalid  # type: ignore[comparison-overlap]
