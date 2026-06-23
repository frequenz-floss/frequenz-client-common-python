# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Delivery area information for the energy market."""

import warnings
from dataclasses import dataclass
from typing import assert_never

from frequenz.core.enum import Enum, deprecated_member, unique

from .._exception import UnrecognizedValueError, UnspecifiedValueError


@unique
class EnergyMarketCodeType(Enum):
    """The identification code types used in the energy market.

    CodeType specifies the type of identification code used for uniquely
    identifying various entities such as delivery areas, market participants,
    and grid components within the energy market.

    This enumeration aims to
    offer compatibility across different jurisdictional standards.

    Note: Understanding Code Types
        Different regions or countries may have their own standards for uniquely
        identifying various entities within the energy market. For example, in
        Europe, the Energy Identification Code (EIC) is commonly used for this
        purpose.

    Note: Extensibility
        New code types can be added to this enum to accommodate additional regional
        standards, enhancing the API's adaptability.

    Danger: Validation Required
        The chosen code type should correspond correctly with the `code` field in
        the relevant message objects, such as `DeliveryArea` or `Counterparty`.
        Failure to match the code type with the correct code could lead to
        processing errors.
    """

    UNSPECIFIED = deprecated_member(
        0,
        "EnergyMarketCodeType.UNSPECIFIED is deprecated; use the `int` value `0` "
        "instead if you really need to check for this low-level value.",
    )
    """Unspecified type. This value is a placeholder and should not be used."""

    EUROPE_EIC = 1
    """European Energy Identification Code Standard."""

    US_NERC = 2
    """North American Electric Reliability Corporation identifiers."""


@dataclass(frozen=True, kw_only=True)
class DeliveryArea:
    """A geographical or administrative region where electricity deliveries occur.

    DeliveryArea represents the geographical or administrative region, usually defined
    and maintained by a Transmission System Operator (TSO), where electricity deliveries
    for a contract occur.

    The concept is important to energy trading as it delineates the agreed-upon delivery
    location. Delivery areas can have different codes based on the jurisdiction in
    which they operate.

    Note: Jurisdictional Differences
        This is typically represented by specific codes according to local jurisdiction.

        In Europe, this is represented by an
        [EIC](https://en.wikipedia.org/wiki/Energy_Identification_Code) (Energy
        Identification Code). [List of
        EICs](https://www.entsoe.eu/data/energy-identification-codes-eic/eic-approved-codes/).
    """

    code: str | None
    """The code representing the unique identifier for the delivery area."""

    code_type: EnergyMarketCodeType | int
    """Type of code used for identifying the delivery area itself.

    This code could be extended in the future, in case an unknown code type is
    encountered, a plain integer value is used to represent it.

    This is the lower-level, forward-compatible accessor; prefer
    `DeliveryArea.get_code_type()` to obtain a known member or a clear error.
    """

    def __str__(self) -> str:
        """Return a human-readable string representation of this instance."""
        code = self.code or "<NO CODE>"
        code_type = (
            f"type={self.code_type}"
            if isinstance(self.code_type, int)
            else self.code_type.name
        )
        return f"{code}[{code_type}]"

    def get_code_type(self) -> EnergyMarketCodeType:
        """Return the code type as a known enum member.

        This is the higher-level accessor for the `code_type` attribute: it
        resolves the value to a known `EnergyMarketCodeType` member or raises a
        clear, catchable error.

        Returns:
            The code type, when it is a known `EnergyMarketCodeType` member.

        Raises:
            UnspecifiedValueError: If the code type is unspecified.
            UnrecognizedValueError: If the code type is a value not recognized by
                this version of the client. The raw value is available on the
                exception's `value` attribute.
        """
        # Suppressing the deprecation warning can be removed when UNSPECIFIED is removed
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            match self.code_type:
                case 0 | EnergyMarketCodeType.UNSPECIFIED:
                    raise UnspecifiedValueError(f"code type of {self} is unspecified")
                case EnergyMarketCodeType() as code_type:
                    return code_type
                case int() as code_type:
                    raise UnrecognizedValueError(
                        code_type,
                        f"code type {code_type!r} of {self} is not a recognized "
                        "EnergyMarketCodeType",
                    )
                case unknown:
                    assert_never(unknown)
