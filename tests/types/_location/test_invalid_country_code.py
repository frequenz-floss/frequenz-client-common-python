# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the InvalidCountryCode wrapper type."""

from frequenz.client.common.types import InvalidCountryCode


def test_stores_value() -> None:
    """`InvalidCountryCode` stores the raw value verbatim."""
    assert InvalidCountryCode(value="DEU").value == "DEU"


def test_equality() -> None:
    """Two `InvalidCountryCode` with the same value are equal and hash the same."""
    a = InvalidCountryCode(value="DEU")
    b = InvalidCountryCode(value="DEU")
    assert a == b
    assert hash(a) == hash(b)


def test_str() -> None:
    """`InvalidCountryCode.__str__` renders with a compact invalid marker."""
    assert str(InvalidCountryCode(value="DEU")) == "<invalid:'DEU'>"
