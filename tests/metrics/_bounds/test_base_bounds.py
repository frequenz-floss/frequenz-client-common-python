# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for `BaseBounds`."""

import pytest

from frequenz.client.common.metrics import BaseBounds


def test_cannot_be_instantiated_directly() -> None:
    """`BaseBounds` refuses direct instantiation."""
    with pytest.raises(TypeError, match="Cannot instantiate BaseBounds directly"):
        BaseBounds()
