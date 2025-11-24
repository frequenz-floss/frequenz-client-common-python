# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for enum_from_proto utility."""

import enum

import pytest

from frequenz.client.common.enum_proto import enum_from_proto


class _TestEnum(enum.Enum):
    """A test enum for enum_from_proto tests."""

    ZERO = 0
    ONE = 1
    TWO = 2


@pytest.mark.parametrize("enum_member", _TestEnum)
def test_deprecated(enum_member: _TestEnum) -> None:
    """Test conversion of valid enum values."""
    with pytest.deprecated_call():
        enum_from_proto(enum_member.value, _TestEnum)
