# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Microgrid type."""

from datetime import datetime, timezone

import pytest

from frequenz.client.common import UnspecifiedValueError
from frequenz.client.common.grid import DeliveryArea, EnergyMarketCodeType
from frequenz.client.common.microgrid import EnterpriseId, Microgrid, MicrogridId
from frequenz.client.common.types import Location


def test_creation() -> None:
    """Test Microgrid creation with all fields."""
    now = datetime.now(timezone.utc)
    info = Microgrid(
        id=MicrogridId(1234),
        enterprise_id=EnterpriseId(5678),
        name="Test Microgrid",
        delivery_area=DeliveryArea(
            code="DE123", code_type=EnergyMarketCodeType.EUROPE_EIC
        ),
        location=Location(latitude=52.52, longitude=13.405, country_code="DE"),
        create_time=now,
        _active=True,
    )

    assert info.id == MicrogridId(1234)
    assert info.enterprise_id == EnterpriseId(5678)
    assert info.name == "Test Microgrid"
    assert info.delivery_area is not None
    assert info.delivery_area.code == "DE123"
    assert info.delivery_area.code_type == EnergyMarketCodeType.EUROPE_EIC
    assert info.location is not None
    assert info.location.latitude is not None
    assert info.location.latitude == pytest.approx(52.52)
    assert info.location.longitude is not None
    assert info.location.longitude == pytest.approx(13.405)
    assert info.location.country_code == "DE"
    assert info.create_time == now
    assert info.is_active() is True


def test_creation_without_optionals() -> None:
    """Test Microgrid creation with only required fields."""
    now = datetime.now(timezone.utc)
    info = Microgrid(
        id=MicrogridId(1234),
        enterprise_id=EnterpriseId(5678),
        name=None,
        delivery_area=None,
        location=None,
        create_time=now,
        _active=True,
    )

    assert info.id == MicrogridId(1234)
    assert info.enterprise_id == EnterpriseId(5678)
    assert info.name is None
    assert info.delivery_area is None
    assert info.location is None
    assert info.create_time == now
    assert info.is_active() is True


@pytest.mark.parametrize(
    "active",
    [
        pytest.param(True, id="active"),
        pytest.param(False, id="inactive"),
    ],
)
def test_is_active(active: bool) -> None:
    """Test the is_active method for known active states."""
    now = datetime.now(timezone.utc)
    info = Microgrid(
        id=MicrogridId(1234),
        enterprise_id=EnterpriseId(5678),
        name=None,
        delivery_area=None,
        location=None,
        create_time=now,
        _active=active,
    )
    assert info.is_active() is active


def test_is_active_unspecified() -> None:
    """Test that is_active raises when the active state is unspecified."""
    now = datetime.now(timezone.utc)
    info = Microgrid(
        id=MicrogridId(1234),
        enterprise_id=EnterpriseId(5678),
        name=None,
        delivery_area=None,
        location=None,
        create_time=now,
        _active=None,
    )
    with pytest.raises(UnspecifiedValueError):
        info.is_active()


@pytest.mark.parametrize(
    "name,expected_str",
    [
        pytest.param("Test Grid", "MID1234:Test Grid", id="with-name"),
        pytest.param(None, "MID1234", id="none-name"),
        pytest.param("", "MID1234", id="empty-name"),
    ],
)
def test_str(name: str | None, expected_str: str) -> None:
    """Test string representation of Microgrid."""
    now = datetime.now(timezone.utc)
    info = Microgrid(
        id=MicrogridId(1234),
        enterprise_id=EnterpriseId(5678),
        name=name,
        delivery_area=None,
        location=None,
        create_time=now,
        _active=True,
    )
    assert str(info) == expected_str
