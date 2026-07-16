# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Base electrical component from which all other electrical components inherit."""

import dataclasses
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self, assert_never

from ..._exception import UnrecognizedEnumValueError, UnspecifiedEnumValueError
from ...metrics import Bounds, InvalidBounds, Metric
from .. import MicrogridId
from .._lifetime import InvalidLifetime, InvalidLifetimeError, Lifetime
from ._ids import ElectricalComponentId


@dataclasses.dataclass(frozen=True, kw_only=True)
class ElectricalComponent:  # pylint: disable=too-many-instance-attributes
    """A base class for all electrical components."""

    id: ElectricalComponentId
    """This electrical component's ID."""

    microgrid_id: MicrogridId
    """The ID of the microgrid this electrical component belongs to."""

    name: str
    """The name of this electrical component."""

    model: str
    """The model of this electrical component.

    This includes both the manufacturer and the model name.
    """

    operational_lifetime: Lifetime | InvalidLifetime = dataclasses.field(
        default_factory=Lifetime
    )
    """The operational lifetime of this electrical component.

    An [`InvalidLifetime`][....InvalidLifetime] preserves malformed wire data.

    Tip:
        Prefer [`get_operational_lifetime()`][..get_operational_lifetime] when
        a valid lifetime is required.
    """

    _provides_telemetry: bool | int
    """Whether this component provides telemetry data.

    This stores the low-level representation of the operational mode. It holds a bool
    for the telemetry part for a known operational mode, the raw `int` `0` when the
    operational mode is unspecified, or any other raw `int` not yet known to this
    client. Users should use
    [`ElectricalComponent.provides_telemetry()`][.provides_telemetry] to obtain a clear
    boolean or a clear error.
    """

    _accepts_control: bool | int
    """Whether this component accepts control commands.

    This stores the low-level representation of the operational mode. It holds a bool
    for a known operational mode, the raw `int` `0` when the operational mode is
    unspecified, or any other raw `int` not yet known to this client. Users should use
    [`ElectricalComponent.accepts_control()`][.accepts_control] to obtain a clear
    boolean or a clear error.
    """

    _allow_construction: bool = dataclasses.field(
        default=False, repr=False, compare=False, hash=False
    )
    """Internal guard allowing construction only via the `*_from_proto` converters."""

    metric_config_bounds: Mapping[Metric | int, Bounds | InvalidBounds] = (
        dataclasses.field(
            default_factory=dict,
            # dict is not hashable, so we don't use this field to calculate the hash.
            # This shouldn't be a problem since it is very unlikely that two components
            # with all other attributes being equal would have different category
            # specific metadata, so hash collisions should be still very unlikely.
            hash=False,
        )
    )
    """The metric configuration bounds for this electrical component, keyed by metric.

    These bounds may be derived from the component configuration, manufacturer
    limits, or limits of other devices.

    Malformed bounds received from the wire are preserved as
    [`InvalidBounds`][.....metrics.InvalidBounds] instances so callers can
    inspect the raw values without accidentally using them for range checks.
    Entries that named a metric but carried no bounds data at all are stored
    as [`MissingBounds`][.....metrics.MissingBounds] (a subclass of
    `InvalidBounds`), letting callers distinguish "explicitly unbounded" from
    "the server forgot to send bounds".

    If an unspecified metric is received, it is stored as the plain `int` key `0` when
    loading from protobuf. Metrics unknown to this client version may also appear
    as plain `int` keys for forward-compatibility.
    """

    category_specific_metadata: Mapping[str, Any] = dataclasses.field(
        default_factory=dict,
        # dict is not hashable, so we don't use this field to calculate the hash. This
        # shouldn't be a problem since it is very unlikely that two components with all
        # other attributes being equal would have different category specific metadata,
        # so hash collisions should be still very unlikely.
        hash=False,
    )
    """The category specific metadata of this electrical component.

    Note:
        This should not be used normally, it is only useful when accessing a newer
        version of the API where the client doesn't know about the new metadata fields
        yet (i.e. for use with
        [`UnrecognizedElectricalComponent`][...UnrecognizedElectricalComponent]).
    """

    def __new__(cls, *_: Any, **__: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is ElectricalComponent:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)

    def __post_init__(self) -> None:
        """Reject direct construction of this read-only type.

        Raises:
            TypeError: If the instance was not created via the corresponding
                `*_from_proto` converter.
        """
        if not self._allow_construction:
            raise TypeError(
                f"{type(self).__name__} cannot be constructed directly; obtain "
                "instances via the corresponding *_from_proto converter."
            )

    def provides_telemetry(self) -> bool:
        """Check whether this electrical component provides telemetry data.

        Returns:
            Whether this electrical component provides telemetry data.

        Raises:
            UnspecifiedEnumValueError: If the operational mode is unspecified.
            UnrecognizedEnumValueError: If the operational mode is not recognized.
                The raw value is available on the error's `value` attribute.
        """
        match self._provides_telemetry:
            case bool() as provides_telemetry:
                return provides_telemetry
            case 0:
                raise UnspecifiedEnumValueError(
                    self,
                    "_provides_telemetry",
                    f"operational mode of {self} is unspecified; "
                    "telemetry availability is unknown",
                )
            case int() as value:
                raise UnrecognizedEnumValueError(
                    self,
                    "_provides_telemetry",
                    value,
                    f"operational mode {value!r} of {self} is not a recognized "
                    "ElectricalComponentOperationalMode; telemetry availability "
                    "is unknown",
                )
            case unknown:
                assert_never(unknown)

    def accepts_control(self) -> bool:
        """Check whether this electrical component accepts control commands.

        Returns:
            Whether this electrical component accepts control commands.

        Raises:
            UnspecifiedEnumValueError: If the operational mode is unspecified.
            UnrecognizedEnumValueError: If the operational mode is not recognized.
                The raw value is available on the error's `value` attribute.
        """
        match self._accepts_control:
            case bool() as accepts_control:
                return accepts_control
            case 0:
                raise UnspecifiedEnumValueError(
                    self,
                    "_accepts_control",
                    f"operational mode of {self} is unspecified; "
                    "control availability is unknown",
                )
            case int() as value:
                raise UnrecognizedEnumValueError(
                    self,
                    "_accepts_control",
                    value,
                    f"operational mode {value!r} of {self} is not a recognized "
                    "ElectricalComponentOperationalMode; control availability "
                    "is unknown",
                )
            case unknown:
                assert_never(unknown)

    def get_operational_lifetime(self) -> Lifetime:
        """Return the operational lifetime as a valid `Lifetime`.

        Returns:
            The valid operational lifetime.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        match self.operational_lifetime:
            case InvalidLifetime() as invalid:
                raise InvalidLifetimeError(self, "operational_lifetime", invalid)
            case Lifetime() as valid:
                return valid
            case unknown:
                assert_never(unknown)

    def is_operational_at(self, timestamp: datetime) -> bool:  # noqa: DOC502
        """Check whether this electrical component is operational at a specific timestamp.

        Args:
            timestamp: The timestamp to check.

        Returns:
            Whether this electrical component is operational at the given timestamp.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        return self.get_operational_lifetime().is_operational_at(timestamp)

    def is_operational_now(self) -> bool:  # noqa: DOC502
        """Check whether this electrical component is currently operational.

        Returns:
            Whether this electrical component is operational at the current time.

        Raises:
            InvalidLifetimeError: If malformed lifetime data was received. The
                offending value is available on the exception's `lifetime`
                attribute.
        """
        return self.is_operational_at(datetime.now(timezone.utc))

    @property
    def identity(self) -> tuple[ElectricalComponentId, MicrogridId]:
        """The identity of this electrical component.

        This uses the component ID and microgrid ID to identify an electrical
        component without considering the other attributes, so even if an electrical
        component state changed, the identity remains the same.
        """
        return (self.id, self.microgrid_id)

    def __str__(self) -> str:
        """Return a human-readable string representation of this instance."""
        name = f":{self.name}" if self.name else ""
        return f"{self.id}<{type(self).__name__}>{name}"
