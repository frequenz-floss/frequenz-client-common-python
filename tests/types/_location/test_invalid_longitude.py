# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the InvalidLongitude wrapper type."""

import pytest

from frequenz.client.common.types import InvalidLongitude


def test_stores_value() -> None:
    """`InvalidLongitude` stores the raw value verbatim."""
    assert InvalidLongitude(value=181.0).value == pytest.approx(181.0)


def test_equality() -> None:
    """Two `InvalidLongitude` with the same value are equal and hash the same."""
    a = InvalidLongitude(value=181.0)
    b = InvalidLongitude(value=181.0)
    assert a == b
    assert hash(a) == hash(b)


def test_str() -> None:
    """`InvalidLongitude.__str__` renders with a compact invalid marker."""
    assert str(InvalidLongitude(value=181.0)) == "<invalid:181.00>"
