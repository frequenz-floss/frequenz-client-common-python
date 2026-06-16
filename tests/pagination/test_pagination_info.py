# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for pagination info."""

import pytest

from frequenz.client.common.pagination import PaginationInfo


def test_pagination_info_accepts_zero_total_items() -> None:
    """Zero total items should be accepted."""
    info = PaginationInfo(total_items=0)
    assert info.total_items == 0


def test_pagination_info_accepts_positive_total_items() -> None:
    """Positive total items should be accepted."""
    info = PaginationInfo(total_items=1)
    assert info.total_items == 1


def test_pagination_info_rejects_negative_total_items() -> None:
    """Negative total items should be rejected with the exact message."""
    with pytest.raises(
        ValueError,
        match=r"^total_items must be non-negative, not -1$",
    ):
        PaginationInfo(total_items=-1)
