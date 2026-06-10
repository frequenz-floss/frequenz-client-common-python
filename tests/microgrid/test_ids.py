# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for microgrid-related IDs."""

import pytest
from frequenz.core.id import BaseId

from frequenz.client.common.microgrid import EnterpriseId, MicrogridId
from frequenz.client.common.microgrid.components import ComponentId
from frequenz.client.common.microgrid.electrical_components import ElectricalComponentId
from frequenz.client.common.microgrid.sensors import SensorId


@pytest.mark.parametrize(
    "id_class, prefix",
    [
        (EnterpriseId, "EID"),
        (MicrogridId, "MID"),
        (ElectricalComponentId, "CID"),
        (SensorId, "SID"),
    ],
)
def test_string_representation(id_class: type[BaseId], prefix: str) -> None:
    """Test string representation of IDs."""
    _id = id_class(123)

    assert str(_id) == f"{prefix}123"
    assert repr(_id) == f"{id_class.__name__}(123)"


def test_component_id_deprecated() -> None:
    """Test that the deprecated ComponentId emits a warning and still works."""
    with pytest.deprecated_call():
        _id = ComponentId(123)

    assert str(_id) == "CID123"
    assert repr(_id) == "ComponentId(123)"
