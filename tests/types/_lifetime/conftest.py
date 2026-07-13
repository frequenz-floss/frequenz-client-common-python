# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Fixtures for lifetime tests."""

from datetime import datetime, timezone

import pytest


@pytest.fixture
def present() -> datetime:
    """Provide the current UTC time."""
    return datetime.now(timezone.utc)


@pytest.fixture
def past(present: datetime) -> datetime:
    """Provide a time in the past."""
    return present.replace(year=present.year - 1)


@pytest.fixture
def future(present: datetime) -> datetime:
    """Provide a time in the future."""
    return present.replace(year=present.year + 1)
