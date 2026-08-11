# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the ElectricalComponent base class and its functionality."""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest

from frequenz.client.common import (
    UnrecognizedEnumValueError,
    UnspecifiedEnumValueError,
)
from frequenz.client.common.metrics import (
    Bounds,
    InvalidBounds,
    InvalidBoundsError,
    Metric,
)
from frequenz.client.common.microgrid import (
    InvalidLifetime,
    InvalidLifetimeError,
    Lifetime,
    MicrogridId,
)
from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponent,
    ElectricalComponentId,
)


class _TestElectricalComponent(ElectricalComponent):
    """A simple electrical component implementation for testing."""


def _make_component(
    *,
    operational_lifetime: Lifetime | InvalidLifetime = Lifetime(),
    metric_config_bounds: dict[Metric | int, Bounds | InvalidBounds] | None = None,
) -> _TestElectricalComponent:
    """Build a test component with the given operational lifetime."""
    if metric_config_bounds is None:
        metric_config_bounds = {}
    return _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        name="",
        model="Test Model",
        metric_config_bounds=metric_config_bounds,
        operational_lifetime=operational_lifetime,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )


def test_base_creation_fails() -> None:
    """Test that ElectricalComponent base class cannot be instantiated directly."""
    with pytest.raises(
        TypeError, match="Cannot instantiate ElectricalComponent directly"
    ):
        _ = ElectricalComponent(
            id=ElectricalComponentId(1),
            microgrid_id=MicrogridId(1),
            name="",
            model="Test Model",
            _provides_telemetry=True,
            _accepts_control=True,
        )


def test_direct_construction_without_flag_raises() -> None:
    """Test that a concrete component cannot be built without the construction flag."""
    with pytest.raises(TypeError, match="cannot be constructed directly"):
        _TestElectricalComponent(
            id=ElectricalComponentId(1),
            microgrid_id=MicrogridId(2),
            name="",
            model="Test Model",
            _provides_telemetry=True,
            _accepts_control=True,
        )


def test_creation_with_defaults() -> None:
    """Test electrical component default values."""
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        name="",
        model="Test Model",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.name == ""
    assert component.model == "Test Model"
    assert component.operational_lifetime == Lifetime()
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
        name="test-component",
        model="Test Manufacturer Test Model",
        metric_config_bounds=metric_config_bounds,
        category_specific_metadata=metadata,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.name == "test-component"
    assert component.model == "Test Manufacturer Test Model"
    assert component.metric_config_bounds == metric_config_bounds
    assert component.category_specific_metadata == metadata


def test_accessors_return_values_when_set() -> None:
    """Test that telemetry/control accessors return the stored booleans."""
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        name="",
        model="Test Model",
        _provides_telemetry=True,
        _accepts_control=False,
        _allow_construction=True,
    )

    assert component.provides_telemetry() is True
    assert component.accepts_control() is False


def test_accessors_raise_when_unspecified() -> None:
    """Test that accessors raise UnspecifiedEnumValueError for the raw int `0`."""
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        name="",
        model="Test Model",
        _provides_telemetry=0,
        _accepts_control=0,
        _allow_construction=True,
    )

    with pytest.raises(UnspecifiedEnumValueError):
        component.provides_telemetry()
    with pytest.raises(UnspecifiedEnumValueError):
        component.accepts_control()


def test_accessors_raise_when_unrecognized() -> None:
    """Test that accessors raise UnrecognizedEnumValueError for an unknown int."""
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        name="",
        model="Test Model",
        _provides_telemetry=999,
        _accepts_control=999,
        _allow_construction=True,
    )

    with pytest.raises(UnrecognizedEnumValueError) as exc_info:
        component.provides_telemetry()
    assert exc_info.value.value == 999
    with pytest.raises(UnrecognizedEnumValueError) as exc_info:
        component.accepts_control()
    assert exc_info.value.value == 999


def test_get_operational_lifetime_returns_valid() -> None:
    """`get_operational_lifetime()` returns a valid lifetime unchanged."""
    lifetime = Lifetime()
    component = _make_component(operational_lifetime=lifetime)

    assert component.get_operational_lifetime() is lifetime


def test_get_operational_lifetime_raises_invalid() -> None:
    """`get_operational_lifetime()` raises with the malformed lifetime attached."""
    invalid = InvalidLifetime(
        start_time=datetime(2025, 2, 1, tzinfo=timezone.utc),
        end_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    component = _make_component(operational_lifetime=invalid)

    with pytest.raises(InvalidLifetimeError) as exc_info:
        component.get_operational_lifetime()
    assert exc_info.value.lifetime is invalid


def test_is_operational_at_raises_for_invalid_lifetime() -> None:
    """`is_operational_at()` raises when the lifetime is invalid."""
    component = _make_component(
        operational_lifetime=InvalidLifetime(
            start_time=datetime(2025, 2, 1, tzinfo=timezone.utc),
            end_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
    )

    with pytest.raises(InvalidLifetimeError):
        component.is_operational_at(datetime(2025, 1, 1, tzinfo=timezone.utc))


def test_is_operational_now_raises_for_invalid_lifetime() -> None:
    """`is_operational_now()` raises when the lifetime is invalid."""
    component = _make_component(
        operational_lifetime=InvalidLifetime(
            start_time=datetime(2025, 2, 1, tzinfo=timezone.utc),
            end_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
    )

    with pytest.raises(InvalidLifetimeError):
        component.is_operational_now()


def test_get_metric_config_bounds_returns_valid_bounds() -> None:
    """`get_metric_config_bounds` returns the configured `Bounds` for a metric."""
    bounds = Bounds(lower=-10.0, upper=10.0)
    component = _make_component(metric_config_bounds={Metric.AC_POWER_ACTIVE: bounds})

    result = component.get_metric_config_bounds(Metric.AC_POWER_ACTIVE)

    assert result is bounds


def test_get_metric_config_bounds_absent_returns_unbounded() -> None:
    """`get_metric_config_bounds` returns an unbounded `Bounds` for absent metrics."""
    component = _make_component(metric_config_bounds={})

    result = component.get_metric_config_bounds(Metric.AC_POWER_ACTIVE)

    assert result == Bounds()
    assert isinstance(result, Bounds)


def test_get_metric_config_bounds_absent_returns_default() -> None:
    """`get_metric_config_bounds` returns `default` for absent metrics."""
    component = _make_component(metric_config_bounds={})
    sentinel = object()

    assert (
        component.get_metric_config_bounds(Metric.AC_POWER_ACTIVE, default=None) is None
    )
    assert (
        component.get_metric_config_bounds(Metric.AC_POWER_ACTIVE, default=sentinel)
        is sentinel
    )


def test_get_metric_config_bounds_present_ignores_default() -> None:
    """`get_metric_config_bounds` ignores `default` when the metric has bounds."""
    bounds = Bounds(lower=-10.0, upper=10.0)
    component = _make_component(metric_config_bounds={Metric.AC_POWER_ACTIVE: bounds})

    assert (
        component.get_metric_config_bounds(Metric.AC_POWER_ACTIVE, default=None)
        is bounds
    )


def test_get_metric_config_bounds_invalid_raises_error() -> None:
    """`get_metric_config_bounds` raises `InvalidBoundsError` for malformed entries."""
    invalid = InvalidBounds(lower=10.0, upper=-10.0)
    component = _make_component(metric_config_bounds={Metric.AC_POWER_ACTIVE: invalid})

    with pytest.raises(InvalidBoundsError) as exc_info:
        component.get_metric_config_bounds(Metric.AC_POWER_ACTIVE)

    assert exc_info.value.bounds is invalid
    assert "AC_POWER_ACTIVE" in str(exc_info.value)


def test_get_metric_config_bounds_invalid_raises_despite_default() -> None:
    """`default` only applies to absent metrics, not malformed ones."""
    invalid = InvalidBounds(lower=10.0, upper=-10.0)
    component = _make_component(metric_config_bounds={Metric.AC_POWER_ACTIVE: invalid})

    with pytest.raises(InvalidBoundsError):
        component.get_metric_config_bounds(Metric.AC_POWER_ACTIVE, default=None)


@pytest.mark.parametrize(
    "name,expected_str",
    [
        ("", "CID1<_TestElectricalComponent>"),
        ("test-component", "CID1<_TestElectricalComponent>:test-component"),
    ],
    ids=["no-name", "with-name"],
)
def test_str(name: str, expected_str: str) -> None:
    """Test string representation of an electrical component."""
    component = _TestElectricalComponent(
        id=ElectricalComponentId(1),
        microgrid_id=MicrogridId(2),
        name=name,
        model="Test Model",
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
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
        name="",
        model="Test Model",
        operational_lifetime=mock_lifetime,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
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
        name="",
        model="Test Model",
        operational_lifetime=mock_lifetime,
        _provides_telemetry=True,
        _accepts_control=True,
        _allow_construction=True,
    )

    assert component.is_operational_now() is True

    mock_lifetime.is_operational_at.assert_called_once_with(now)


COMPONENT = _TestElectricalComponent(
    id=ElectricalComponentId(1),
    microgrid_id=MicrogridId(1),
    name="test",
    model="Test Model",
    metric_config_bounds={Metric.AC_POWER_ACTIVE: Bounds(lower=-100.0, upper=100.0)},
    category_specific_metadata={"key": "value"},
    _provides_telemetry=True,
    _accepts_control=True,
    _allow_construction=True,
)

DIFFERENT_NONHASHABLE = _TestElectricalComponent(
    id=COMPONENT.id,
    microgrid_id=COMPONENT.microgrid_id,
    name=COMPONENT.name,
    model=COMPONENT.model,
    metric_config_bounds={Metric.AC_POWER_ACTIVE: Bounds(lower=-200.0, upper=200.0)},
    category_specific_metadata={"different": "metadata"},
    _provides_telemetry=True,
    _accepts_control=True,
    _allow_construction=True,
)

DIFFERENT_NAME = _TestElectricalComponent(
    id=COMPONENT.id,
    microgrid_id=COMPONENT.microgrid_id,
    name="different",
    model=COMPONENT.model,
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
    _provides_telemetry=True,
    _accepts_control=True,
    _allow_construction=True,
)

DIFFERENT_ID = _TestElectricalComponent(
    id=ElectricalComponentId(2),
    microgrid_id=COMPONENT.microgrid_id,
    name=COMPONENT.name,
    model=COMPONENT.model,
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
    _provides_telemetry=True,
    _accepts_control=True,
    _allow_construction=True,
)

DIFFERENT_MICROGRID_ID = _TestElectricalComponent(
    id=COMPONENT.id,
    microgrid_id=MicrogridId(2),
    name=COMPONENT.name,
    model=COMPONENT.model,
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
    _provides_telemetry=True,
    _accepts_control=True,
    _allow_construction=True,
)

DIFFERENT_BOTH_ID = _TestElectricalComponent(
    id=ElectricalComponentId(2),
    microgrid_id=MicrogridId(2),
    name=COMPONENT.name,
    model=COMPONENT.model,
    metric_config_bounds=COMPONENT.metric_config_bounds,
    category_specific_metadata=COMPONENT.category_specific_metadata,
    _provides_telemetry=True,
    _accepts_control=True,
    _allow_construction=True,
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
