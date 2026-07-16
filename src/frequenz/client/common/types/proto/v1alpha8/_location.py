# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Loading of Location objects from protobuf messages."""

from frequenz.api.common.v1alpha8.types import location_pb2

from ..._location import (
    InvalidCountryCode,
    InvalidLatitude,
    InvalidLongitude,
    Location,
)


def location_from_proto(message: location_pb2.Location) -> Location:
    """Convert a protobuf message to a [`Location`][....Location] object.

    The returned instance carries the raw wire values with the following
    normalization applied:

    * Latitude and longitude are wrapped in
      [`InvalidLatitude`][....InvalidLatitude] and
      [`InvalidLongitude`][....InvalidLongitude] respectively when they
      fall outside their well-formed ranges.
    * An empty `country_code` on the wire is normalized to `None`; a
      non-empty `country_code` that is not exactly 2 characters long is
      wrapped in [`InvalidCountryCode`][....InvalidCountryCode].

    Use the `get_*()` accessors on the returned instance to obtain
    validated values or a clear `InvalidAttributeError` subclass.

    Args:
        message: The protobuf message to convert.

    Returns:
        The resulting [`Location`][....Location] object.
    """
    latitude: float | InvalidLatitude = (
        message.latitude
        if -90.0 <= message.latitude <= 90.0
        else InvalidLatitude(value=message.latitude)
    )
    longitude: float | InvalidLongitude = (
        message.longitude
        if -180.0 <= message.longitude <= 180.0
        else InvalidLongitude(value=message.longitude)
    )
    country_code: str | InvalidCountryCode | None
    if not message.country_code:
        country_code = None
    elif len(message.country_code) == 2:
        country_code = message.country_code
    else:
        country_code = InvalidCountryCode(value=message.country_code)
    return Location(latitude=latitude, longitude=longitude, country_code=country_code)
