# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the category specific info carried by electrical components."""

from frequenz.client.common.microgrid.electrical_components import (
    CategorySpecificInfo,
)


def test_construction() -> None:
    """The kind and leftover fields are exposed as given."""
    info = CategorySpecificInfo(kind="battery", fields={"foo": "bar"})

    assert info.kind == "battery"
    assert info.fields == {"foo": "bar"}


def test_fields_default_to_empty() -> None:
    """The leftover fields default to an empty mapping."""
    info = CategorySpecificInfo(kind="inverter")

    assert info.fields == {}


def test_equality() -> None:
    """Equality considers both the kind and the leftover fields."""
    a = CategorySpecificInfo(kind="battery", fields={"x": 1})
    b = CategorySpecificInfo(kind="battery", fields={"x": 1})
    c = CategorySpecificInfo(kind="battery", fields={"x": 2})
    d = CategorySpecificInfo(kind="inverter", fields={"x": 1})

    assert a == b
    assert a != c
    assert a != d


def test_equal_instances_hash_equally() -> None:
    """Instances equal by content hash equally and dedupe in a set."""
    a = CategorySpecificInfo(kind="battery", fields={"x": 1, "y": 2})
    b = CategorySpecificInfo(kind="battery", fields={"y": 2, "x": 1})

    assert a == b
    assert hash(a) == hash(b)
    assert len({a, b}) == 1


def test_equal_values_hash_equally_regardless_of_type() -> None:
    """Values that compare equal but repr differently still hash equally.

    Guards against deriving the hash from ``repr(value)``: ``1``, ``1.0`` and
    ``True`` compare equal, so instances carrying them must hash equally and
    deduplicate in a set (equal objects are required to have equal hashes).
    """
    a = CategorySpecificInfo(kind="battery", fields={"x": 1})
    b = CategorySpecificInfo(kind="battery", fields={"x": 1.0})
    c = CategorySpecificInfo(kind="battery", fields={"x": True})

    assert a == b == c
    assert hash(a) == hash(b) == hash(c)
    assert len({a, b, c}) == 1


def test_hashable_with_unhashable_values() -> None:
    """Fields carrying unhashable values can still be hashed."""
    info = CategorySpecificInfo(kind="battery", fields={"x": [1, 2]})

    assert isinstance(hash(info), int)
