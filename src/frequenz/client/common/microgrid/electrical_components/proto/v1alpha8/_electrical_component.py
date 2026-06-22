# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Conversion of electrical components to/from protobuf v1alpha8."""

import logging
import warnings
from collections.abc import Sequence
from typing import Any, NamedTuple, assert_never

from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)
from google.protobuf.json_format import MessageToDict

from .....metrics import Bounds, Metric
from .....metrics.proto.v1alpha8 import bounds_from_proto
from .....proto import enum_from_proto
from .....types import Lifetime
from .....types.proto.v1alpha8 import lifetime_from_proto
from ...._ids import MicrogridId
from ... import (
    AcEvCharger,
    BatteryInverter,
    BatteryType,
    Breaker,
    Chp,
    Converter,
    CryptoMiner,
    DcEvCharger,
    ElectricalComponentCategory,
    ElectricalComponentId,
    ElectricalComponentTypes,
    Electrolyzer,
    EvChargerType,
    GridConnectionPoint,
    Hvac,
    HybridEvCharger,
    HybridInverter,
    InverterType,
    LiIonBattery,
    Meter,
    MismatchedCategoryElectricalComponent,
    NaIonBattery,
    PowerTransformer,
    Precharger,
    PvInverter,
    SteamBoiler,
    UnrecognizedBattery,
    UnrecognizedElectricalComponent,
    UnrecognizedEvCharger,
    UnrecognizedInverter,
    UnspecifiedBattery,
    UnspecifiedElectricalComponent,
    UnspecifiedEvCharger,
    UnspecifiedInverter,
    WindTurbine,
)

_logger = logging.getLogger(__name__)


# We disable the `too-many-arguments` check in the whole file because all _from_proto
# functions are expected to take many arguments.
# pylint: disable=too-many-arguments


_BOOLS_BY_OPERATIONAL_MODE: dict[int, tuple[bool | None, bool | None]] = {
    electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_INACTIVE: (
        False,
        False,
    ),
    electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_TELEMETRY_ONLY: (
        True,
        False,
    ),
    electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_CONTROL_ONLY: (
        False,
        True,
    ),
    electrical_components_pb2.ELECTRICAL_COMPONENT_OPERATIONAL_MODE_CONTROL_AND_TELEMETRY: (
        True,
        True,
    ),
}


def _operational_mode_to_bools(value: int) -> tuple[bool | None, bool | None]:
    """Map a protobuf operational mode to telemetry/control booleans.

    Args:
        value: A protobuf operational-mode enum value (an
            `ELECTRICAL_COMPONENT_OPERATIONAL_MODE_*` constant).

    Returns:
        A `(provides_telemetry, accepts_control)` tuple, with both elements `None`
            when the operational mode is unspecified or unrecognized.
    """
    return _BOOLS_BY_OPERATIONAL_MODE.get(value, (None, None))


def electrical_component_from_proto(
    message: electrical_components_pb2.ElectricalComponent,
) -> ElectricalComponentTypes:
    """Convert a protobuf message to an electrical component instance.

    Args:
        message: The protobuf message.

    Returns:
        The resulting electrical component instance.
    """
    major_issues: list[str] = []
    minor_issues: list[str] = []

    component = electrical_component_from_proto_with_issues(
        message, major_issues=major_issues, minor_issues=minor_issues
    )

    if major_issues:
        _logger.warning(
            "Found issues in electrical component: %s | Protobuf message:\n%s",
            ", ".join(major_issues),
            message,
        )
    if minor_issues:
        _logger.debug(
            "Found minor issues in electrical component: %s | Protobuf message:\n%s",
            ", ".join(minor_issues),
            message,
        )

    return component


class _ElectricalComponentBaseData(NamedTuple):
    """Base data for an electrical component, extracted from a protobuf message."""

    component_id: ElectricalComponentId
    """The unique identifier of the electrical component."""

    microgrid_id: MicrogridId
    """The unique identifier of the parent microgrid."""

    name: str | None
    """The optional human-readable name of the electrical component."""

    model: str | None
    """The optional model string of the electrical component."""

    category: ElectricalComponentCategory | int
    """The category of the electrical component."""

    lifetime: Lifetime
    """The operational lifetime of the electrical component."""

    metric_config_bounds: dict[Metric | int, Bounds]
    """The metric configuration bounds extracted from the protobuf message."""

    category_specific_info: dict[str, Any]
    """The category-specific metadata extracted from the protobuf message."""

    provides_telemetry: bool | None
    """Whether the electrical component provides telemetry, or `None` if unknown."""

    accepts_control: bool | None
    """Whether the electrical component accepts control, or `None` if unknown."""

    category_mismatched: bool = False
    """Whether the declared category and the carried metadata disagree."""


# pylint: disable-next=too-many-locals
def _electrical_component_base_from_proto_with_issues(
    message: electrical_components_pb2.ElectricalComponent,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> _ElectricalComponentBaseData:
    """Extract base data from a protobuf message and collect issues.

    Args:
        message: The protobuf message.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        An `_ElectricalComponentBaseData` named tuple containing the extracted data.
    """
    component_id = ElectricalComponentId(message.id)
    microgrid_id = MicrogridId(message.microgrid_id)

    name = message.name or None
    if name is None:
        minor_issues.append("name is empty")

    model = message.model or None
    if model is None:
        minor_issues.append("model is empty")

    provides_telemetry, accepts_control = _operational_mode_to_bools(
        message.operational_mode
    )

    lifetime = _get_operational_lifetime_from_proto(
        message, major_issues=major_issues, minor_issues=minor_issues
    )

    metric_config_bounds = _metric_config_bounds_from_proto(
        message.metric_config_bounds,
        major_issues=major_issues,
        minor_issues=minor_issues,
    )

    category = enum_from_proto(message.category, ElectricalComponentCategory)
    if category is ElectricalComponentCategory.UNSPECIFIED:
        major_issues.append("category is unspecified")
    elif isinstance(category, int):
        major_issues.append(f"category {category} is unrecognized")

    category_specific_info_kind = message.category_specific_info.WhichOneof("kind")
    category_specific_info: dict[str, Any] = {}
    if category_specific_info_kind is not None:
        category_specific_info = MessageToDict(
            getattr(message.category_specific_info, category_specific_info_kind),
            always_print_fields_with_no_presence=True,
        )

    category_mismatched = False
    if (
        category_specific_info_kind
        and isinstance(category, ElectricalComponentCategory)
        and category.name.lower() != category_specific_info_kind
    ):
        major_issues.append(
            f"category_specific_info.kind ({category_specific_info_kind}) does not "
            f"match the category ({category.name.lower()})",
        )
        category_mismatched = True

    return _ElectricalComponentBaseData(
        component_id,
        microgrid_id,
        name,
        model,
        category,
        lifetime,
        metric_config_bounds,
        category_specific_info,
        provides_telemetry,
        accepts_control,
        category_mismatched,
    )


# pylint: disable-next=too-many-locals, too-many-branches
def electrical_component_from_proto_with_issues(
    message: electrical_components_pb2.ElectricalComponent,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> ElectricalComponentTypes:
    """Convert a protobuf message to an electrical component and collect issues.

    Args:
        message: The protobuf message.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The resulting electrical component instance.
    """
    base_data = _electrical_component_base_from_proto_with_issues(
        message, major_issues=major_issues, minor_issues=minor_issues
    )

    if base_data.category_mismatched:
        return MismatchedCategoryElectricalComponent(
            id=base_data.component_id,
            microgrid_id=base_data.microgrid_id,
            name=base_data.name,
            model=base_data.model,
            category=base_data.category,
            operational_lifetime=base_data.lifetime,
            _provides_telemetry=base_data.provides_telemetry,
            _accepts_control=base_data.accepts_control,
            _allow_construction=True,
            category_specific_metadata=base_data.category_specific_info,
            metric_config_bounds=base_data.metric_config_bounds,
        )

    match base_data.category:
        case int():
            return UnrecognizedElectricalComponent(
                id=base_data.component_id,
                microgrid_id=base_data.microgrid_id,
                name=base_data.name,
                model=base_data.model,
                category=base_data.category,
                operational_lifetime=base_data.lifetime,
                _provides_telemetry=base_data.provides_telemetry,
                _accepts_control=base_data.accepts_control,
                _allow_construction=True,
                metric_config_bounds=base_data.metric_config_bounds,
            )
        case (
            ElectricalComponentCategory.UNSPECIFIED
            | ElectricalComponentCategory.CHP
            | ElectricalComponentCategory.CONVERTER
            | ElectricalComponentCategory.CRYPTO_MINER
            | ElectricalComponentCategory.ELECTROLYZER
            | ElectricalComponentCategory.HVAC
            | ElectricalComponentCategory.METER
            | ElectricalComponentCategory.PRECHARGER
            | ElectricalComponentCategory.BREAKER
            | ElectricalComponentCategory.STEAM_BOILER
            | ElectricalComponentCategory.WIND_TURBINE
        ):
            return _trivial_category_to_class(base_data.category)(
                id=base_data.component_id,
                microgrid_id=base_data.microgrid_id,
                name=base_data.name,
                model=base_data.model,
                operational_lifetime=base_data.lifetime,
                _provides_telemetry=base_data.provides_telemetry,
                _accepts_control=base_data.accepts_control,
                _allow_construction=True,
                metric_config_bounds=base_data.metric_config_bounds,
            )
        case ElectricalComponentCategory.BATTERY:
            battery_enum_to_class: dict[
                BatteryType, type[UnspecifiedBattery | LiIonBattery | NaIonBattery]
            ] = {
                BatteryType.UNSPECIFIED: UnspecifiedBattery,
                BatteryType.LI_ION: LiIonBattery,
                BatteryType.NA_ION: NaIonBattery,
            }
            battery_type = enum_from_proto(
                message.category_specific_info.battery.type, BatteryType
            )
            match battery_type:
                case BatteryType.UNSPECIFIED | BatteryType.LI_ION | BatteryType.NA_ION:
                    if battery_type is BatteryType.UNSPECIFIED:
                        major_issues.append("battery type is unspecified")
                    return battery_enum_to_class[battery_type](
                        id=base_data.component_id,
                        microgrid_id=base_data.microgrid_id,
                        name=base_data.name,
                        model=base_data.model,
                        operational_lifetime=base_data.lifetime,
                        _provides_telemetry=base_data.provides_telemetry,
                        _accepts_control=base_data.accepts_control,
                        _allow_construction=True,
                        metric_config_bounds=base_data.metric_config_bounds,
                    )
                case int():
                    major_issues.append(f"battery type {battery_type} is unrecognized")
                    return UnrecognizedBattery(
                        id=base_data.component_id,
                        microgrid_id=base_data.microgrid_id,
                        name=base_data.name,
                        model=base_data.model,
                        operational_lifetime=base_data.lifetime,
                        _provides_telemetry=base_data.provides_telemetry,
                        _accepts_control=base_data.accepts_control,
                        _allow_construction=True,
                        metric_config_bounds=base_data.metric_config_bounds,
                        type=battery_type,
                    )
                case unexpected_battery_type:
                    assert_never(unexpected_battery_type)
        case ElectricalComponentCategory.EV_CHARGER:
            ev_charger_enum_to_class: dict[
                EvChargerType,
                type[
                    UnspecifiedEvCharger | AcEvCharger | DcEvCharger | HybridEvCharger
                ],
            ] = {
                EvChargerType.UNSPECIFIED: UnspecifiedEvCharger,
                EvChargerType.AC: AcEvCharger,
                EvChargerType.DC: DcEvCharger,
                EvChargerType.HYBRID: HybridEvCharger,
            }
            ev_charger_type = enum_from_proto(
                message.category_specific_info.ev_charger.type, EvChargerType
            )
            match ev_charger_type:
                case (
                    EvChargerType.UNSPECIFIED
                    | EvChargerType.AC
                    | EvChargerType.DC
                    | EvChargerType.HYBRID
                ):
                    if ev_charger_type is EvChargerType.UNSPECIFIED:
                        major_issues.append("ev_charger type is unspecified")
                    return ev_charger_enum_to_class[ev_charger_type](
                        id=base_data.component_id,
                        microgrid_id=base_data.microgrid_id,
                        name=base_data.name,
                        model=base_data.model,
                        operational_lifetime=base_data.lifetime,
                        _provides_telemetry=base_data.provides_telemetry,
                        _accepts_control=base_data.accepts_control,
                        _allow_construction=True,
                        metric_config_bounds=base_data.metric_config_bounds,
                    )
                case int():
                    major_issues.append(
                        f"ev_charger type {ev_charger_type} is unrecognized"
                    )
                    return UnrecognizedEvCharger(
                        id=base_data.component_id,
                        microgrid_id=base_data.microgrid_id,
                        name=base_data.name,
                        model=base_data.model,
                        operational_lifetime=base_data.lifetime,
                        _provides_telemetry=base_data.provides_telemetry,
                        _accepts_control=base_data.accepts_control,
                        _allow_construction=True,
                        metric_config_bounds=base_data.metric_config_bounds,
                        type=ev_charger_type,
                    )
                case unexpected_ev_charger_type:
                    assert_never(unexpected_ev_charger_type)
        case ElectricalComponentCategory.GRID_CONNECTION_POINT:
            rated_fuse_current = (
                message.category_specific_info.grid_connection_point.rated_fuse_current
            )
            # No need to check for negatives because the protobuf type is uint32.
            return GridConnectionPoint(
                id=base_data.component_id,
                microgrid_id=base_data.microgrid_id,
                name=base_data.name,
                model=base_data.model,
                operational_lifetime=base_data.lifetime,
                _provides_telemetry=base_data.provides_telemetry,
                _accepts_control=base_data.accepts_control,
                _allow_construction=True,
                metric_config_bounds=base_data.metric_config_bounds,
                rated_fuse_current=rated_fuse_current,
            )
        case ElectricalComponentCategory.INVERTER:
            inverter_enum_to_class: dict[
                InverterType,
                type[
                    UnspecifiedInverter | BatteryInverter | PvInverter | HybridInverter
                ],
            ] = {
                InverterType.UNSPECIFIED: UnspecifiedInverter,
                InverterType.BATTERY: BatteryInverter,
                InverterType.PV: PvInverter,
                InverterType.HYBRID: HybridInverter,
            }
            inverter_type = enum_from_proto(
                message.category_specific_info.inverter.type, InverterType
            )
            match inverter_type:
                case (
                    InverterType.UNSPECIFIED
                    | InverterType.BATTERY
                    | InverterType.PV
                    | InverterType.HYBRID
                ):
                    if inverter_type is InverterType.UNSPECIFIED:
                        major_issues.append("inverter type is unspecified")
                    return inverter_enum_to_class[inverter_type](
                        id=base_data.component_id,
                        microgrid_id=base_data.microgrid_id,
                        name=base_data.name,
                        model=base_data.model,
                        operational_lifetime=base_data.lifetime,
                        _provides_telemetry=base_data.provides_telemetry,
                        _accepts_control=base_data.accepts_control,
                        _allow_construction=True,
                        metric_config_bounds=base_data.metric_config_bounds,
                    )
                case int():
                    major_issues.append(
                        f"inverter type {inverter_type} is unrecognized"
                    )
                    return UnrecognizedInverter(
                        id=base_data.component_id,
                        microgrid_id=base_data.microgrid_id,
                        name=base_data.name,
                        model=base_data.model,
                        operational_lifetime=base_data.lifetime,
                        _provides_telemetry=base_data.provides_telemetry,
                        _accepts_control=base_data.accepts_control,
                        _allow_construction=True,
                        metric_config_bounds=base_data.metric_config_bounds,
                        type=inverter_type,
                    )
                case unexpected_inverter_type:
                    assert_never(unexpected_inverter_type)
        case ElectricalComponentCategory.POWER_TRANSFORMER:
            return PowerTransformer(
                id=base_data.component_id,
                microgrid_id=base_data.microgrid_id,
                name=base_data.name,
                model=base_data.model,
                operational_lifetime=base_data.lifetime,
                _provides_telemetry=base_data.provides_telemetry,
                _accepts_control=base_data.accepts_control,
                _allow_construction=True,
                metric_config_bounds=base_data.metric_config_bounds,
                primary_voltage=message.category_specific_info.power_transformer.primary,
                secondary_voltage=message.category_specific_info.power_transformer.secondary,
            )
        case (
            ElectricalComponentCategory.PLC
            | ElectricalComponentCategory.STATIC_TRANSFER_SWITCH
            | ElectricalComponentCategory.UNINTERRUPTIBLE_POWER_SUPPLY
            | ElectricalComponentCategory.CAPACITOR_BANK
        ):
            major_issues.append(
                f"category {base_data.category.name} has no specific electrical "
                "component type"
            )
            return UnrecognizedElectricalComponent(
                id=base_data.component_id,
                microgrid_id=base_data.microgrid_id,
                name=base_data.name,
                model=base_data.model,
                category=base_data.category.value,
                operational_lifetime=base_data.lifetime,
                _provides_telemetry=base_data.provides_telemetry,
                _accepts_control=base_data.accepts_control,
                _allow_construction=True,
                metric_config_bounds=base_data.metric_config_bounds,
            )
        case unexpected_category:
            assert_never(unexpected_category)


def _trivial_category_to_class(
    category: ElectricalComponentCategory,
) -> type[
    UnspecifiedElectricalComponent
    | Breaker
    | Chp
    | Converter
    | CryptoMiner
    | Electrolyzer
    | Hvac
    | Meter
    | Precharger
    | SteamBoiler
    | WindTurbine
]:
    """Return the class corresponding to a trivial electrical component category."""
    return {
        ElectricalComponentCategory.UNSPECIFIED: UnspecifiedElectricalComponent,
        ElectricalComponentCategory.CHP: Chp,
        ElectricalComponentCategory.CONVERTER: Converter,
        ElectricalComponentCategory.CRYPTO_MINER: CryptoMiner,
        ElectricalComponentCategory.ELECTROLYZER: Electrolyzer,
        ElectricalComponentCategory.HVAC: Hvac,
        ElectricalComponentCategory.METER: Meter,
        ElectricalComponentCategory.PRECHARGER: Precharger,
        ElectricalComponentCategory.BREAKER: Breaker,
        ElectricalComponentCategory.STEAM_BOILER: SteamBoiler,
        ElectricalComponentCategory.WIND_TURBINE: WindTurbine,
    }[category]


def _metric_config_bounds_from_proto(
    message: Sequence[electrical_components_pb2.MetricConfigBounds],
    *,
    major_issues: list[str],
    minor_issues: list[str],  # pylint: disable=unused-argument
) -> dict[Metric | int, Bounds]:
    """Convert a `MetricConfigBounds` message to a dictionary mapping `Metric` to `Bounds`.

    The keys of the result map are
    [`Metric`][frequenz.client.common.metrics.Metric] enum members (or `int` for
    unrecognized values) and the values are
    [`Bounds`][frequenz.client.common.metrics.Bounds] objects.

    Args:
        message: The `MetricConfigBounds` message.
        major_issues: A list to append major issues to.
        minor_issues: A list to append minor issues to.

    Returns:
        The resulting dictionary mapping metrics to their bounds.
    """
    bounds: dict[Metric | int, Bounds] = {}
    for metric_bound in message:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            metric = enum_from_proto(metric_bound.metric, Metric)
            match metric:
                case Metric.UNSPECIFIED:
                    metric = metric.value
                case int():
                    minor_issues.append(
                        f"metric_config_bounds has an unrecognized metric {metric}"
                    )

        if not metric_bound.HasField("config_bounds"):
            major_issues.append(
                f"metric_config_bounds for {metric} is present but missing "
                "`config_bounds`, considering it unbounded",
            )
            continue

        try:
            bound = bounds_from_proto(metric_bound.config_bounds)
        except ValueError as exc:
            major_issues.append(
                f"metric_config_bounds for {metric} is invalid ({exc}), considering "
                "it as missing (i.e. unbouded)",
            )
            continue
        if metric in bounds:
            major_issues.append(
                f"metric_config_bounds for {metric} is duplicated in the message"
                f"using the last one ({bound})",
            )
        bounds[metric] = bound

    return bounds


def _get_operational_lifetime_from_proto(
    message: electrical_components_pb2.ElectricalComponent,
    *,
    major_issues: list[str],
    minor_issues: list[str],
) -> Lifetime:
    """Get the operational lifetime from a protobuf message.

    Args:
        message: The protobuf message to extract the operational lifetime from.
        major_issues: A list to collect major issues found during parsing.
        minor_issues: A list to collect minor issues found during parsing.

    Returns:
        The extracted operational lifetime, or an empty lifetime if the protobuf
            field is missing or invalid.
    """
    if message.HasField("operational_lifetime"):
        try:
            return lifetime_from_proto(message.operational_lifetime)
        except ValueError as exc:
            major_issues.append(
                f"invalid operational lifetime ({exc}), considering it as missing "
                "(i.e. always operational)",
            )
    else:
        minor_issues.append(
            "missing operational lifetime, considering it always operational",
        )
    return Lifetime()
