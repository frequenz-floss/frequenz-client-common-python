# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `BaseLifetime`."""

import pytest

from frequenz.client.common.microgrid import BaseLifetime


def test_cannot_be_instantiated_directly() -> None:
    """`BaseLifetime` refuses direct instantiation."""
    with pytest.raises(TypeError, match="Cannot instantiate BaseLifetime directly"):
        BaseLifetime()
