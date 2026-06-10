# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the Microgrid type."""

from datetime import datetime, timezone

import pytest

from frequenz.client.common.grid import DeliveryArea, EnergyMarketCodeType
from frequenz.client.common.microgrid import (
    EnterpriseId,
    Microgrid,
    MicrogridId,
    MicrogridStatus,
)
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
        status=MicrogridStatus.ACTIVE,
        create_timestamp=now,
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
    assert info.status == MicrogridStatus.ACTIVE
    assert info.create_timestamp == now
    assert info.is_active is True


def test_creation_without_optionals() -> None:
    """Test Microgrid creation with only required fields."""
    now = datetime.now(timezone.utc)
    info = Microgrid(
        id=MicrogridId(1234),
        enterprise_id=EnterpriseId(5678),
        name=None,
        delivery_area=None,
        location=None,
        status=MicrogridStatus.ACTIVE,
        create_timestamp=now,
    )

    assert info.id == MicrogridId(1234)
    assert info.enterprise_id == EnterpriseId(5678)
    assert info.name is None
    assert info.delivery_area is None
    assert info.location is None
    assert info.status == MicrogridStatus.ACTIVE
    assert info.create_timestamp == now
    assert info.is_active is True


@pytest.mark.parametrize(
    "status,expected_active",
    [
        pytest.param(MicrogridStatus.ACTIVE, True, id="ACTIVE"),
        pytest.param(MicrogridStatus.INACTIVE, False, id="INACTIVE"),
        pytest.param(MicrogridStatus.UNSPECIFIED, True, id="UNSPECIFIED"),
    ],
)
def test_is_active_property(status: MicrogridStatus, expected_active: bool) -> None:
    """Test the is_active property for different status values."""
    now = datetime.now(timezone.utc)
    info = Microgrid(
        id=MicrogridId(1234),
        enterprise_id=EnterpriseId(5678),
        name=None,
        delivery_area=None,
        location=None,
        status=status,
        create_timestamp=now,
    )
    assert info.is_active is expected_active


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
        status=MicrogridStatus.ACTIVE,
        create_timestamp=now,
    )
    assert str(info) == expected_str
