# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Shared parity and conversion test base class for protobuf-backed enums.

Every Python enum that mirrors a protobuf enum follows the same convention:

* The protobuf enum value name is a fixed prefix (e.g. `EVENT_`) followed by
  the Python enum member name.
* The protobuf enum value number matches the Python enum value.
* There is a versioned `<enum>_from_proto` function returning the Python
  enum member for known values and the raw [`int`][] for unknown values.
* There is a versioned `<enum>_to_proto` function returning the numeric
  protobuf value.

[`EnumParityTest`][.EnumParityTest] is a parametrized [`pytest`][pytest]
base class covering all those invariants. New enum wrappers add a one-line
subclass that pins the protobuf-specific attributes instead of copy-pasting
the same scaffold.
"""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from typing import Any, ClassVar

import pytest


class EnumParityTest:
    """Base test class checking protobuf/Python enum parity.

    Subclasses must set [`python_enum`][.python_enum],
    [`proto_enum`][.proto_enum], [`name_prefix`][.name_prefix],
    [`from_proto`][.from_proto] and [`to_proto`][.to_proto]. The subclass
    name must start with `Test` so [`pytest`][pytest] picks it up.

    For each subclass, the inherited tests verify that:

    * every protobuf enum name maps to a Python enum member with the same value
      (tolerating new protobuf values not yet mirrored in Python);
    * every Python enum member maps to a protobuf enum name and value;
    * [`from_proto`][.from_proto] returns the matching member for known values
      and the raw [`int`][] for unknown values;
    * [`to_proto`][.to_proto] returns the numeric protobuf value.

    Subclasses are free to add further `test_*` methods.

    Example:
        ```python
        from frequenz.api.common.v1alpha8.streaming import event_pb2

        from frequenz.client.common.streaming import Event
        from frequenz.client.common.streaming.proto.v1alpha8 import (
            event_from_proto,
            event_to_proto,
        )

        from frequenz.client.common.test.enum_parity import EnumParityTest


        class TestEventParity(EnumParityTest):
            python_enum = Event
            proto_enum = event_pb2.Event
            name_prefix = "EVENT_"
            from_proto = staticmethod(event_from_proto)
            to_proto = staticmethod(event_to_proto)
        ```
    """

    python_enum: ClassVar[type[Enum]]
    """The Python enum subclass mirroring the protobuf enum."""

    proto_enum: ClassVar[Any]
    """The generated protobuf enum wrapper (e.g. `event_pb2.Event`).

    Must expose `DESCRIPTOR.values`, `Value(name)`, `Name(value)` and
    `ValueType`.
    """

    name_prefix: ClassVar[str]
    """Prefix used for protobuf enum value names (e.g. `"EVENT_"`)."""

    from_proto: ClassVar[Callable[..., Any]]
    """Versioned converter from a protobuf enum value to the Python enum.

    Returns the Python enum member for known values, or the raw [`int`][] for
    unknown values. Bind with `staticmethod(...)` in the subclass.
    """

    to_proto: ClassVar[Callable[..., int]]
    """Versioned converter from a Python enum member to a protobuf enum value.

    Bind with `staticmethod(...)` in the subclass.
    """

    def pytest_generate_tests(self, metafunc: pytest.Metafunc) -> None:
        """Parametrize `pb_name` and `member` from the configured enums.

        Args:
            metafunc: The `pytest` metafunc object for the test being collected.
        """
        if "pb_name" in metafunc.fixturenames:
            pb_names = [m.name for m in self.proto_enum.DESCRIPTOR.values]
            metafunc.parametrize("pb_name", pb_names)
        if "member" in metafunc.fixturenames:
            members = list(self.python_enum)
            metafunc.parametrize("member", members, ids=lambda m: m.name)

    def test_proto_enum_matches_enum_name(self, pb_name: str) -> None:
        """Test that all known protobuf enum names match a Python member.

        Args:
            pb_name: The protobuf enum value name to check.
        """
        pb_value = self.proto_enum.Value(pb_name)
        try:
            member = self.python_enum[pb_name.removeprefix(self.name_prefix)]
        except KeyError:
            # It is OK to have new protobuf enum values not yet in the Python
            # enum.
            return
        assert member.value == pb_value

    def test_proto_enum_matches_enum_value(self, pb_name: str) -> None:
        """Test that all known protobuf enum values match a Python member.

        Args:
            pb_name: The protobuf enum value name to check.
        """
        pb_value = self.proto_enum.Value(pb_name)
        try:
            member = self.python_enum(pb_value)
        except ValueError:
            # It is OK to have new protobuf enum values not yet in the Python
            # enum.
            return
        assert member.value == pb_value

    def test_enum_matches_proto_enum_name(self, member: Enum) -> None:
        """Test that all Python enum members have a matching protobuf name.

        Args:
            member: The Python enum member to check.
        """
        pb_value = self.proto_enum.ValueType(member.value)
        pb_name = self.proto_enum.Name(pb_value)
        assert pb_name == f"{self.name_prefix}{member.name}"

    def test_enum_matches_proto_enum_value(self, member: Enum) -> None:
        """Test that all Python enum members have a matching protobuf value.

        Args:
            member: The Python enum member to check.
        """
        pb_value = self.proto_enum.Value(f"{self.name_prefix}{member.name}")
        assert member.value == pb_value

    def test_from_proto(self, pb_name: str) -> None:
        """Test conversion from protobuf returns a matching member or int.

        Args:
            pb_name: The protobuf enum value name to convert.
        """
        pb_value = self.proto_enum.Value(pb_name)
        result = self.from_proto(pb_value)
        if pb_value in [m.value for m in self.python_enum]:
            assert result is self.python_enum(pb_value)
        else:
            assert result == pb_value

    def test_from_proto_unknown(self) -> None:
        """Test conversion from protobuf for unknown values returns the int."""
        max_value = max(m.value for m in self.python_enum)
        unknown_pb_value = self.proto_enum.ValueType(max_value + 1)
        result = self.from_proto(unknown_pb_value)
        assert isinstance(result, int)
        assert result == unknown_pb_value

    def test_to_proto(self, member: Enum) -> None:
        """Test conversion to protobuf returns a matching protobuf value.

        Args:
            member: The Python enum member to convert.
        """
        pb_value = self.to_proto(member)
        assert pb_value == member.value
