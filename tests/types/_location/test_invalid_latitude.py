# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the InvalidLatitude wrapper type."""

import pytest

from frequenz.client.common.types import InvalidLatitude


def test_stores_value() -> None:
    """`InvalidLatitude` stores the raw value verbatim."""
    assert InvalidLatitude(value=91.0).value == pytest.approx(91.0)


def test_equality() -> None:
    """Two `InvalidLatitude` with the same value are equal and hash the same."""
    a = InvalidLatitude(value=91.0)
    b = InvalidLatitude(value=91.0)
    assert a == b
    assert hash(a) == hash(b)


def test_str() -> None:
    """`InvalidLatitude.__str__` renders with a compact invalid marker."""
    assert str(InvalidLatitude(value=91.0)) == "<invalid:91.00>"
