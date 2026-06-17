# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the ElectricalComponent base class and its functionality."""

from datetime import datetime, timezone
from typing import Literal
from unittest.mock import Mock, patch

import pytest

from frequenz.client.common.metrics import Bounds, Metric
from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponent,
    ElectricalComponentCategory,
    ElectricalComponentId,
    ElectricalComponentOperationalMode,
)
from frequenz.client.common.types import Lifetime


class _TestElectricalComponent(ElectricalComponent):
    """A simple electrical component implementation for testing."""

    category: Literal[ElectricalComponentCategory.UNSPECIFIED] = (
        ElectricalComponentCategory.UNSPECIFIED
    )


def test_base_creation_fails() -> None:
    """Test that ElectricalComponent base class cannot be instantiated directly."""
    with pytest.raises(
        TypeError, match="Cannot instantiate ElectricalComponent directly"
    ):
        _ = ElectricalComponent(
            id=ElectricalComponentId(1),
            microgrid_id=MicrogridId(1),
            category=ElectricalComponentCategory.UNSPECIFIED,
        )


def test_creation_with_defaults() -> None:
    """Test electrical component default values."""
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        category=ElectricalComponentCategory.UNSPECIFIED,
    )

    assert component.name is None
    assert component.model is None
    assert component.operational_lifetime == Lifetime()
    assert component.operational_mode == ElectricalComponentOperationalMode.UNSPECIFIED
    assert component.metric_config_bounds == {}
    assert component.category_specific_metadata == {}


def test_creation_full() -> None:
    """Test electrical component creation with all attributes."""
    bounds = Bounds(lower=-100.0, upper=100.0)
    metric_config_bounds: dict[Metric | int, Bounds] = {Metric.AC_POWER_ACTIVE: bounds}
    metadata = {"key1": "value1", "key2": 42}

    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        category=ElectricalComponentCategory.UNSPECIFIED,
        name="test-component",
        model="Test Manufacturer Test Model",
        metric_config_bounds=metric_config_bounds,
        category_specific_metadata=metadata,
    )

    assert component.name == "test-component"
    assert component.model == "Test Manufacturer Test Model"
    assert component.metric_config_bounds == metric_config_bounds
    assert component.category_specific_metadata == metadata


@pytest.mark.parametrize(
    "name,expected_str",
    [
        (None, "CID1<_TestElectricalComponent>"),
        ("test-component", "CID1<_TestElectricalComponent>:test-component"),
    ],
    ids=["no-name", "with-name"],
)
def test_str(name: str | None, expected_str: str) -> None:
    """Test string representation of an electrical component."""
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        category=ElectricalComponentCategory.UNSPECIFIED,
        name=name,
    )
    assert str(component) == expected_str


@pytest.mark.parametrize(
    "is_operational", [True, False], ids=["operational", "not-operational"]
)
def test_operational_at(is_operational: bool) -> None:
    """Test active_at behavior with lifetime combinations."""
    mock_lifetime = Mock(spec=Lifetime)
    mock_lifetime.is_operational_at.return_value = is_operational

    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(1),
        category=ElectricalComponentCategory.UNSPECIFIED,
        operational_lifetime=mock_lifetime,
    )

    test_time = datetime.now(timezone.utc)
    assert component.is_operational_at(test_time) == is_operational

    mock_lifetime.is_operational_at.assert_called_once_with(test_time)


@patch(
    "frequenz.client.common.microgrid.electrical_components"
    "._electrical_component.datetime"
)
def test_is_operational_now(mock_datetime: Mock) -> None:
    """Test is_active_now method."""
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.side_effect = lambda tz: now.replace(tzinfo=tz)
    mock_lifetime = Mock(spec=Lifetime)
    mock_lifetime.is_operational_at.return_value = True
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(1),
        category=ElectricalComponentCategory.UNSPECIFIED,
        operational_lifetime=mock_lifetime,
    )

    assert component.is_operational_now() is True

    mock_lifetime.is_operational_at.assert_called_once_with(now)


COMPONENT = _TestElectricalComponent(
    id=ElectricalComponentId(1),
    microgrid_id=MicrogridId(1),
    category=ElectricalComponentCategory.UNSPECIFIED,
    name="test",
    metric_config_bounds={Metric.AC_POWER_ACTIVE: Bounds(lower=-100.0, upper=100.0)},
    category_specific_metadata={"key": "value"},
)

DIFFERENT_NONHASHABLE = _TestElectricalComponent(
    id=COMPONENT.id,
    microgrid_id=COMPONENT.microgrid_id,
    category=COMPONENT.category,
    name=COMPONENT.name,
    metric_config_bounds={Metric.AC_POWER_ACTIVE: Bounds(lower=-200.0, upper=200.0)},
    category_specific_metadata={"different": "metadata"},
)

DIFFERENT_NAME = _TestElectricalComponent(
    id=COMPONENT.id,
    microgrid_id=COMPONENT.microgrid_id,
    category=COMPONENT.category,
    name="different",
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
)

DIFFERENT_ID = _TestElectricalComponent(
    id=ElectricalComponentId(2),
    microgrid_id=COMPONENT.microgrid_id,
    category=COMPONENT.category,
    name=COMPONENT.name,
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
)

DIFFERENT_MICROGRID_ID = _TestElectricalComponent(
    id=COMPONENT.id,
    microgrid_id=MicrogridId(2),
    category=COMPONENT.category,
    name=COMPONENT.name,
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
)

DIFFERENT_BOTH_ID = _TestElectricalComponent(
    id=ElectricalComponentId(2),
    microgrid_id=MicrogridId(2),
    category=COMPONENT.category,
    name=COMPONENT.name,
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
)


@pytest.mark.parametrize(
    "comp,expected",
    [
        pytest.param(COMPONENT, True, id="self"),
        pytest.param(DIFFERENT_NONHASHABLE, False, id="other-nonhashable"),
        pytest.param(DIFFERENT_NAME, False, id="other-name"),
        pytest.param(DIFFERENT_ID, False, id="other-id"),
        pytest.param(DIFFERENT_MICROGRID_ID, False, id="other-microgrid-id"),
        pytest.param(DIFFERENT_BOTH_ID, False, id="other-both-ids"),
    ],
    ids=lambda o: str(o.id) if isinstance(o, ElectricalComponent) else str(o),
)
def test_equality(comp: ElectricalComponent, expected: bool) -> None:
    """Test electrical component equality."""
    assert (COMPONENT == comp) is expected
    assert (comp == COMPONENT) is expected
    assert (COMPONENT != comp) is not expected
    assert (comp != COMPONENT) is not expected


@pytest.mark.parametrize(
    "comp,expected",
    [
        pytest.param(COMPONENT, True, id="self"),
        pytest.param(DIFFERENT_NONHASHABLE, True, id="other-nonhashable"),
        pytest.param(DIFFERENT_NAME, True, id="other-name"),
        pytest.param(DIFFERENT_ID, False, id="other-id"),
        pytest.param(DIFFERENT_MICROGRID_ID, False, id="other-microgrid-id"),
        pytest.param(DIFFERENT_BOTH_ID, False, id="other-both-ids"),
    ],
)
def test_identity(comp: ElectricalComponent, expected: bool) -> None:
    """Test electrical component identity."""
    assert (COMPONENT.identity == comp.identity) is expected
    assert comp.identity == (comp.id, comp.microgrid_id)


ALL_COMPONENTS_PARAMS = [
    pytest.param(COMPONENT, id="comp"),
    pytest.param(DIFFERENT_NONHASHABLE, id="nonhashable"),
    pytest.param(DIFFERENT_NAME, id="name"),
    pytest.param(DIFFERENT_ID, id="id"),
    pytest.param(DIFFERENT_MICROGRID_ID, id="microgrid_id"),
    pytest.param(DIFFERENT_BOTH_ID, id="both_ids"),
]


@pytest.mark.parametrize("comp1", ALL_COMPONENTS_PARAMS)
@pytest.mark.parametrize("comp2", ALL_COMPONENTS_PARAMS)
def test_hash(comp1: ElectricalComponent, comp2: ElectricalComponent) -> None:
    """Test that the hash is consistent."""
    # We can only say the hash are the same if the components are equal, if they
    # are not, they could still have the same hash (and they will if they have
    # only different non-hashable attributes)
    if comp1 == comp2:
        assert hash(comp1) == hash(comp2)
