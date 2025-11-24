# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for enum_from_proto utility."""

import enum

import pytest

from frequenz.client.common.proto import enum_from_proto


class _TestEnum(enum.Enum):
    """A test enum for enum_from_proto tests."""

    ZERO = 0
    ONE = 1
    TWO = 2


@pytest.mark.parametrize("enum_member", _TestEnum)
def test_valid_allow_invalid(enum_member: _TestEnum) -> None:
    """Test conversion of valid enum values."""
    assert enum_from_proto(enum_member.value, _TestEnum) == enum_member
    assert (
        enum_from_proto(enum_member.value, _TestEnum, allow_invalid=True) == enum_member
    )


@pytest.mark.parametrize("value", [42, -1])
def test_invalid_allow_invalid(value: int) -> None:
    """Test unknown values with allow_invalid=True (default)."""
    assert enum_from_proto(value, _TestEnum) == value
    assert enum_from_proto(value, _TestEnum, allow_invalid=True) == value


@pytest.mark.parametrize("enum_member", _TestEnum)
def test_valid_disallow_invalid(enum_member: _TestEnum) -> None:
    """Test unknown values with allow_invalid=False (should raise ValueError)."""
    assert (
        enum_from_proto(enum_member.value, _TestEnum, allow_invalid=False)
        == enum_member
    )


@pytest.mark.parametrize("value", [42, -1])
def test_invalid_disallow(value: int) -> None:
    """Test unknown values with allow_invalid=False (should raise ValueError)."""
    with pytest.raises(ValueError, match=rf"^{value} is not a valid _TestEnum$"):
        enum_from_proto(value, _TestEnum, allow_invalid=False)
