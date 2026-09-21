# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for microgrid-related IDs."""

import base64
import importlib
import os
import pickle
import subprocess
import sys
from pathlib import Path

import pytest
from frequenz.core.id import BaseId

from frequenz.client.common.microgrid import EnterpriseId, MicrogridId
from frequenz.client.common.microgrid.components import ComponentId
from frequenz.client.common.microgrid.electrical_components import ElectricalComponentId
from frequenz.client.common.microgrid.sensors import SensorId

# Trusted fixture generated from the released v0.3.8 tag (peeled commit
# 66b890388c47412006c6767c6c3fcdd69c187c5d) with:
# uv run --extra dev-pytest python -c 'import base64,pickle; from
# frequenz.client.common.microgrid.components import ComponentId; print(
# base64.b64encode(pickle.dumps(ComponentId(123))).decode())'
_V0_3_8_COMPONENT_ID_PICKLE = base64.b64decode(
    "gAWVTgAAAAAAAACMK2ZyZXF1ZW56LmNsaWVudC5jb21tb24ubWljcm9ncmlkLmNvbXBvbmVudHOU"
    "jAtDb21wb25lbnRJZJSTlCmBlH2UjANfaWSUS3tzYi4="
)


@pytest.mark.parametrize(
    "id_class, prefix",
    [
        (EnterpriseId, "EID"),
        (MicrogridId, "MID"),
        (ElectricalComponentId, "ECID"),
        (SensorId, "SID"),
    ],
)
def test_string_representation(id_class: type[BaseId], prefix: str) -> None:
    """Test string representation of IDs."""
    _id = id_class(123)

    assert str(_id) == f"{prefix}123"
    assert repr(_id) == f"{id_class.__name__}(123)"


def test_component_id_is_a_distinct_deprecated_type() -> None:
    """Test the restored component ID type remains distinct from its replacement."""
    with pytest.deprecated_call():
        component_id = ComponentId(123)
    electrical_component_id = ElectricalComponentId(123)
    with pytest.deprecated_call():
        same_component_id = ComponentId(123)

    assert component_id != electrical_component_id
    assert not isinstance(component_id, ElectricalComponentId)
    assert not isinstance(electrical_component_id, ComponentId)
    assert {component_id, electrical_component_id} == {
        same_component_id,
        ElectricalComponentId(123),
    }
    assert {component_id: "old", electrical_component_id: "new"} == {
        same_component_id: "old",
        ElectricalComponentId(123): "new",
    }


def test_component_id_equality_and_validation() -> None:
    """Test equality, hashing and validation for component IDs."""
    with pytest.deprecated_call():
        first = ComponentId(123)
    with pytest.deprecated_call():
        second = ComponentId(123)

    assert first == second
    assert hash(first) == hash(second)
    assert int(first) == 123
    assert str(first) == "CID123"
    assert repr(first) == "ComponentId(123)"

    with pytest.deprecated_call():
        with pytest.raises(ValueError, match="ComponentId can't be negative"):
            ComponentId(-1)


@pytest.mark.parametrize(
    "imports",
    [
        (
            "from frequenz.client.common.microgrid.components import ComponentId\n"
            "from frequenz.client.common.microgrid.electrical_components "
            "import ElectricalComponentId"
        ),
        (
            "from frequenz.client.common.microgrid.electrical_components "
            "import ElectricalComponentId\n"
            "from frequenz.client.common.microgrid.components import ComponentId"
        ),
    ],
)
def test_component_id_import_orders_produce_no_prefix_warning(imports: str) -> None:
    """Test both import orders emit no duplicate-prefix warning.

    ElectricalComponentId uses ECID and ComponentId uses CID, so they no
    longer share a prefix regardless of import order.
    """
    source_root = Path(__file__).resolve().parents[2] / "src"
    script = f"""
import logging
logging.basicConfig(level=logging.WARNING)
{imports}
assert ComponentId is not ElectricalComponentId
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        path for path in (str(source_root), env.get("PYTHONPATH")) if path
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert "already registered" not in result.stderr


def test_component_id_does_not_restore_legacy_enums() -> None:
    """Test that only the component ID compatibility symbol is restored."""
    module = importlib.import_module("frequenz.client.common.microgrid.components")

    assert not hasattr(module, "ComponentCategory")
    assert not hasattr(module, "ComponentStateCode")
    assert not hasattr(module, "ComponentErrorCode")


def test_component_id_loads_an_old_path_pickle() -> None:
    """Test loading a trusted pickle carrying the historical import path."""
    source_root = Path(__file__).resolve().parents[2] / "src"
    script = """
import base64
import pickle
from frequenz.client.common.microgrid.components import ComponentId

print(base64.b64encode(pickle.dumps(ComponentId(123))).decode())
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        path for path in (str(source_root), env.get("PYTHONPATH")) if path
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    payload = base64.b64decode(result.stdout.strip())
    assert b"frequenz.client.common.microgrid.components" in payload
    assert b"ComponentId" in payload

    with pytest.deprecated_call():
        loaded = pickle.loads(payload)
    # Exact type identity is part of the restored compatibility behavior.
    # pylint: disable-next=unidiomatic-typecheck
    assert type(loaded) is ComponentId
    with pytest.deprecated_call():
        assert loaded == ComponentId(123)


def test_component_id_loads_a_v0_3_8_pickle() -> None:
    """Test loading a pickle generated by the released v0.3.8 class."""
    payload = _V0_3_8_COMPONENT_ID_PICKLE

    assert b"frequenz.client.common.microgrid.components" in payload
    assert b"ComponentId" in payload
    with pytest.deprecated_call():
        loaded = pickle.loads(payload)

    # Exact type identity is part of the restored compatibility behavior.
    # pylint: disable-next=unidiomatic-typecheck
    assert type(loaded) is ComponentId
    with pytest.deprecated_call():
        assert loaded == ComponentId(123)
