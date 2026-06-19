# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Base electrical component from which all other electrical components inherit."""

import dataclasses
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Self

from ..._exception import UnspecifiedValueError
from ...metrics import Bounds, Metric
from ...types import Lifetime
from .. import MicrogridId
from ._category import ElectricalComponentCategory
from ._ids import ElectricalComponentId


@dataclasses.dataclass(frozen=True, kw_only=True)
class ElectricalComponent:  # pylint: disable=too-many-instance-attributes
    """A base class for all electrical components."""

    id: ElectricalComponentId
    """This electrical component's ID."""

    microgrid_id: MicrogridId
    """The ID of the microgrid this electrical component belongs to."""

    category: ElectricalComponentCategory | int
    """The category of this electrical component.

    Note:
        This should not be used normally, you should test if an electrical component
        [`isinstance`][] of a concrete electrical component class instead.

        It is only provided for using with a newer version of the API where the client
        doesn't know about a new category yet (i.e. for use with
        [`UnrecognizedElectricalComponent`][...UnrecognizedElectricalComponent]) and
        in case some low level code needs to know the category of an electrical component.
        """

    name: str | None = None
    """The name of this electrical component."""

    model: str | None = None
    """The model of this electrical component.

    This includes both the manufacturer and the model name.
    """

    operational_lifetime: Lifetime = dataclasses.field(default_factory=Lifetime)
    """The operational lifetime of this electrical component."""

    _provides_telemetry: bool | None
    """Whether this component provides telemetry data, or `None` if unspecified."""

    _accepts_control: bool | None
    """Whether this component accepts control commands, or `None` if unspecified."""

    _allow_construction: bool = dataclasses.field(
        default=False, repr=False, compare=False, hash=False
    )
    """Internal guard allowing construction only via the `*_from_proto` converters."""

    metric_config_bounds: Mapping[Metric | int, Bounds] = dataclasses.field(
        default_factory=dict,
        # dict is not hashable, so we don't use this field to calculate the hash. This
        # shouldn't be a problem since it is very unlikely that two components with all
        # other attributes being equal would have different category specific metadata,
        # so hash collisions should be still very unlikely.
        hash=False,
    )
    """The metric configuration bounds for this electrical component, keyed by metric.

    These bounds may be derived from the component configuration, manufacturer
    limits, or limits of other devices.
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
            UnspecifiedValueError: If the operational mode is unspecified, so whether
                telemetry is provided is unknown.
        """
        if self._provides_telemetry is None:
            raise UnspecifiedValueError(
                f"operational mode of {self} is unspecified; "
                "telemetry availability is unknown"
            )
        return self._provides_telemetry

    def accepts_control(self) -> bool:
        """Check whether this electrical component accepts control commands.

        Returns:
            Whether this electrical component accepts control commands.

        Raises:
            UnspecifiedValueError: If the operational mode is unspecified, so whether
                control commands are accepted is unknown.
        """
        if self._accepts_control is None:
            raise UnspecifiedValueError(
                f"operational mode of {self} is unspecified; "
                "control availability is unknown"
            )
        return self._accepts_control

    def is_operational_at(self, timestamp: datetime) -> bool:
        """Check whether this electrical component is operational at a specific timestamp.

        Args:
            timestamp: The timestamp to check.

        Returns:
            Whether this electrical component is operational at the given timestamp.
        """
        return self.operational_lifetime.is_operational_at(timestamp)

    def is_operational_now(self) -> bool:
        """Check whether this electrical component is currently operational.

        Returns:
            Whether this electrical component is operational at the current time.
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
