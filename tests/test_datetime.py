# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for the `InvalidDatetime` wrapper type and its error."""

from frequenz.client.common import (
    ClientCommonError,
    InvalidAttributeError,
    InvalidDatetime,
    InvalidDatetimeError,
)


def test_stores_raw_numbers() -> None:
    """`InvalidDatetime` stores the raw wire numbers verbatim."""
    invalid = InvalidDatetime(seconds=253402300800, nanos=1)
    assert invalid.seconds == 253402300800
    assert invalid.nanos == 1


def test_equality() -> None:
    """Two `InvalidDatetime` with the same numbers are equal and hash the same."""
    a = InvalidDatetime(seconds=253402300800, nanos=1)
    b = InvalidDatetime(seconds=253402300800, nanos=1)
    assert a == b
    assert hash(a) == hash(b)
    assert a != InvalidDatetime(seconds=253402300800, nanos=2)


def test_str() -> None:
    """`InvalidDatetime.__str__` renders with a compact invalid marker."""
    assert str(InvalidDatetime(seconds=253402300800, nanos=0)) == (
        "<invalid:253402300800s+0ns>"
    )


def test_str_negative_nanos() -> None:
    """A negative fraction keeps its sign, so the two numbers stay readable."""
    assert str(InvalidDatetime(seconds=-1, nanos=-1)) == "<invalid:-1s-1ns>"


def test_error_inherits_invalid_attribute_error() -> None:
    """`InvalidDatetimeError` inherits `InvalidAttributeError` (and thus `ValueError`)."""
    assert issubclass(InvalidDatetimeError, InvalidAttributeError)
    assert issubclass(InvalidDatetimeError, ClientCommonError)
    assert issubclass(InvalidDatetimeError, ValueError)


def test_error_stores_instance_attr_name_and_datetime() -> None:
    """`InvalidDatetimeError` stores `instance`, `attr_name` and `datetime`."""
    instance = object()
    invalid = InvalidDatetime(seconds=253402300800, nanos=0)
    error = InvalidDatetimeError(instance, "sample_time", invalid)
    assert error.instance is instance
    assert error.attr_name == "sample_time"
    assert error.datetime is invalid


def test_error_default_message() -> None:
    """The default message follows the `invalid timestamp ...` template."""
    invalid = InvalidDatetime(seconds=253402300800, nanos=0)
    assert str(InvalidDatetimeError("some-instance", "sample_time", invalid)) == (
        "invalid timestamp <invalid:253402300800s+0ns> for attribute "
        "'sample_time' in some-instance"
    )


def test_error_custom_message_replaces_the_default() -> None:
    """A custom message replaces the default entirely."""
    invalid = InvalidDatetime(seconds=0, nanos=-1)
    assert str(InvalidDatetimeError("i", "a", invalid, "explicit msg")) == (
        "explicit msg"
    )
