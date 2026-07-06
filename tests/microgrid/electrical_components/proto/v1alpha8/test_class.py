# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for electrical component class to/from protobuf v1alpha8 conversion."""

from typing import TypeAlias, cast

import pytest
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2 as ec_pb2,
)

from frequenz.client.common import UnrecognizedEnumValueError
from frequenz.client.common.microgrid import MicrogridId
from frequenz.client.common.microgrid.electrical_components import (
    AcEvCharger,
    Battery,
    BatteryInverter,
    Breaker,
    CapacitorBank,
    Chp,
    Converter,
    CryptoMiner,
    DcEvCharger,
    ElectricalComponent,
    ElectricalComponentId,
    Electrolyzer,
    EvCharger,
    GridConnectionPoint,
    Hvac,
    HybridEvCharger,
    HybridInverter,
    Inverter,
    LiIonBattery,
    Meter,
    MismatchedCategoryElectricalComponent,
    NaIonBattery,
    Plc,
    PowerTransformer,
    Precharger,
    PvInverter,
    StaticTransferSwitch,
    SteamBoiler,
    UninterruptiblePowerSupply,
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
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_class_from_proto,
    electrical_component_class_to_proto,
)

_ProtoCategory: TypeAlias = ec_pb2.ElectricalComponentCategory.ValueType
"""Local alias for the protobuf electrical component category enum value."""

_ProtoSubtype: TypeAlias = (
    ec_pb2.BatteryType.ValueType
    | ec_pb2.EvChargerType.ValueType
    | ec_pb2.InverterType.ValueType
)
"""Local alias for any protobuf electrical component subtype enum value."""


# ---------------------------------------------------------------------------
# Class → proto fixtures
# ---------------------------------------------------------------------------

_CONCRETE_TYPED_CLASS_TO_PROTO: list[tuple[type[ElectricalComponent], int, int]] = [
    (
        LiIonBattery,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
        ec_pb2.BATTERY_TYPE_LI_ION,
    ),
    (
        NaIonBattery,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
        ec_pb2.BATTERY_TYPE_NA_ION,
    ),
    (
        UnspecifiedBattery,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
        ec_pb2.BATTERY_TYPE_UNSPECIFIED,
    ),
    (
        AcEvCharger,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER,
        ec_pb2.EV_CHARGER_TYPE_AC,
    ),
    (
        DcEvCharger,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER,
        ec_pb2.EV_CHARGER_TYPE_DC,
    ),
    (
        HybridEvCharger,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER,
        ec_pb2.EV_CHARGER_TYPE_HYBRID,
    ),
    (
        UnspecifiedEvCharger,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER,
        ec_pb2.EV_CHARGER_TYPE_UNSPECIFIED,
    ),
    (
        BatteryInverter,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER,
        ec_pb2.INVERTER_TYPE_BATTERY,
    ),
    (
        PvInverter,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER,
        ec_pb2.INVERTER_TYPE_PV,
    ),
    (
        HybridInverter,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER,
        ec_pb2.INVERTER_TYPE_HYBRID,
    ),
    (
        UnspecifiedInverter,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER,
        ec_pb2.INVERTER_TYPE_UNSPECIFIED,
    ),
]
"""Concrete typed classes that round-trip with a specific ``(category, subtype)`` pair."""

_ABSTRACT_TYPED_CLASS_TO_PROTO: list[tuple[type[ElectricalComponent], int]] = [
    (Battery, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY),
    (EvCharger, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER),
    (Inverter, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER),
]
"""Abstract typed bases that round-trip with ``subtype=None``."""

_TYPELESS_CLASS_TO_PROTO: list[tuple[type[ElectricalComponent], int]] = [
    (Breaker, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BREAKER),
    (CapacitorBank, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_CAPACITOR_BANK),
    (Chp, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_CHP),
    (Converter, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_CONVERTER),
    (CryptoMiner, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_CRYPTO_MINER),
    (Electrolyzer, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_ELECTROLYZER),
    (GridConnectionPoint, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_GRID_CONNECTION_POINT),
    (Hvac, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_HVAC),
    (Meter, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_METER),
    (Plc, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_PLC),
    (PowerTransformer, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_POWER_TRANSFORMER),
    (Precharger, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_PRECHARGER),
    (StaticTransferSwitch, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_STATIC_TRANSFER_SWITCH),
    (SteamBoiler, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_STEAM_BOILER),
    (
        UninterruptiblePowerSupply,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_UNINTERRUPTIBLE_POWER_SUPPLY,
    ),
    (
        UnspecifiedElectricalComponent,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_UNSPECIFIED,
    ),
    (WindTurbine, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_WIND_TURBINE),
]
"""Typeless classes that round-trip with ``subtype=None``."""

_TO_PROTO_CASES: list[tuple[type[ElectricalComponent], int, int | None]] = [
    *_CONCRETE_TYPED_CLASS_TO_PROTO,
    *[(cls, cat, None) for cls, cat in _ABSTRACT_TYPED_CLASS_TO_PROTO],
    *[(cls, cat, None) for cls, cat in _TYPELESS_CLASS_TO_PROTO],
]
"""All round-trippable classes and their ``(category, subtype)`` proto identity."""


# ---------------------------------------------------------------------------
# Instance helpers
# ---------------------------------------------------------------------------

_BASE_KWARGS: dict[str, object] = {
    "id": ElectricalComponentId(1),
    "microgrid_id": MicrogridId(1),
    "name": "",
    "_provides_telemetry": True,
    "_accepts_control": True,
    "_allow_construction": True,
}
"""Common base kwargs to instantiate any electrical component without runtime guard rails."""

_EXTRA_KWARGS_BY_CLASS: dict[type[ElectricalComponent], dict[str, object]] = {
    GridConnectionPoint: {"rated_fuse_current": 100},
    PowerTransformer: {"primary_voltage": 400.0, "secondary_voltage": 230.0},
}
"""Per-class extra required kwargs for classes that have category-specific fields."""


# ---------------------------------------------------------------------------
# `_to_proto` tests — classes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("component_class", "category", "subtype"),
    _TO_PROTO_CASES,
    ids=lambda value: value.__name__ if isinstance(value, type) else None,
)
def test_class_to_proto_accepts_classes(
    component_class: type[ElectricalComponent], category: int, subtype: int | None
) -> None:
    """Test every round-trippable class encodes to its ``(category, subtype)`` pair."""
    # Given: a round-trippable electrical component class.
    # When: it is converted to its protobuf identity pair.
    result = electrical_component_class_to_proto(
        component_class  # type: ignore[arg-type]
    )

    # Then: the raw protobuf category and subtype match the class identity.
    assert result == (category, subtype)


# ---------------------------------------------------------------------------
# `_to_proto` tests — instances
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("component_class", "category", "subtype"),
    [
        *_CONCRETE_TYPED_CLASS_TO_PROTO,
        *[(cls, cat, None) for cls, cat in _TYPELESS_CLASS_TO_PROTO],
    ],
    ids=lambda value: value.__name__ if isinstance(value, type) else None,
)
def test_class_to_proto_accepts_concrete_instances(
    component_class: type[ElectricalComponent], category: int, subtype: int | None
) -> None:
    """Test every concrete instance encodes to the same ``(category, subtype)`` as its class."""
    # Given: an instance of a concrete electrical component class.
    instance = component_class(
        **_BASE_KWARGS,  # type: ignore[arg-type]
        **_EXTRA_KWARGS_BY_CLASS.get(component_class, {}),  # type: ignore[arg-type]
    )

    # When: it is converted to its protobuf identity pair.
    result = electrical_component_class_to_proto(
        instance  # type: ignore[call-overload]
    )

    # Then: the encoding matches the class encoding.
    assert result == (category, subtype)


@pytest.mark.parametrize(
    ("component_class", "category"),
    [
        (UnrecognizedBattery, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY),
        (UnrecognizedEvCharger, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER),
        (UnrecognizedInverter, ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER),
    ],
    ids=lambda value: value.__name__ if isinstance(value, type) else None,
)
def test_class_to_proto_unrecognized_typed_instance_preserves_subtype(
    component_class: (
        type[UnrecognizedBattery]
        | type[UnrecognizedEvCharger]
        | type[UnrecognizedInverter]
    ),
    category: int,
) -> None:
    """Test the raw `type=` int from a per-family unrecognized instance is preserved."""
    # Given: an Unrecognized* instance whose `type` is an arbitrary out-of-range int.
    instance = component_class(**_BASE_KWARGS, type=999)  # type: ignore[arg-type]

    # When: it is converted to its protobuf identity pair.
    result = electrical_component_class_to_proto(instance)

    # Then: the family category is returned with the raw int subtype intact.
    assert result == (category, 999)


@pytest.mark.parametrize(
    "component_class",
    [UnrecognizedBattery, UnrecognizedEvCharger, UnrecognizedInverter],
    ids=lambda value: value.__name__,
)
def test_class_to_proto_unrecognized_typed_class_returns_none_subtype(
    component_class: (
        type[UnrecognizedBattery]
        | type[UnrecognizedEvCharger]
        | type[UnrecognizedInverter]
    ),
) -> None:
    """Test passing an `Unrecognized*` class loses the raw subtype int."""
    # Given: an `Unrecognized*` family class (no instance, so no `type` int).
    # When: it is converted to its protobuf identity pair.
    category, subtype = electrical_component_class_to_proto(component_class)

    # Then: the family category is returned with `subtype=None` (the raw int is unavailable).
    assert category in {
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER,
        ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER,
    }
    assert subtype is None


def test_class_to_proto_unrecognized_top_level_instance_preserves_category() -> None:
    """Test `UnrecognizedElectricalComponent` instance returns its raw category int."""
    # Given: an `UnrecognizedElectricalComponent` instance with an unrecognized category.
    instance = UnrecognizedElectricalComponent(
        **_BASE_KWARGS,  # type: ignore[arg-type]
        category=999,
    )

    # When: it is converted to its protobuf identity pair.
    result = electrical_component_class_to_proto(instance)

    # Then: the raw int category is preserved, with `subtype=None`.
    assert result == (999, None)


@pytest.mark.parametrize(
    ("instance_category", "expected_category"),
    [
        (int(ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_METER), 2),
        (999, 999),
    ],
    ids=["known-int-category", "unrecognized-int-category"],
)
def test_class_to_proto_mismatched_instance_returns_category_int(
    instance_category: int, expected_category: int
) -> None:
    """Test `MismatchedCategoryElectricalComponent` returns its category as a raw int."""
    # Given: a `MismatchedCategoryElectricalComponent` instance.
    instance = MismatchedCategoryElectricalComponent(
        **_BASE_KWARGS,  # type: ignore[arg-type]
        category=instance_category,
    )

    # When: it is converted to its protobuf identity pair.
    result = electrical_component_class_to_proto(instance)

    # Then: the raw int category is preserved, with `subtype=None`.
    assert result == (expected_category, None)


# ---------------------------------------------------------------------------
# `_to_proto` rejection cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "component_class",
    [UnrecognizedElectricalComponent, MismatchedCategoryElectricalComponent],
    ids=lambda value: value.__name__,
)
def test_class_to_proto_rejects_top_level_problematic_classes(
    component_class: type[ElectricalComponent],
) -> None:
    """Test that top-level problematic classes can't be converted as classes."""
    # Given: a top-level problematic class with no recoverable category.
    # When/Then: converting it raises `TypeError`.
    with pytest.raises(TypeError, match="unsupported electrical component class"):
        electrical_component_class_to_proto(component_class)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# `_from_proto` tests — round-trip with `_to_proto`
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("component_class", "category", "subtype"),
    _TO_PROTO_CASES,
    ids=lambda value: value.__name__ if isinstance(value, type) else None,
)
def test_class_from_proto_round_trips_to_proto(
    component_class: type[ElectricalComponent], category: int, subtype: int | None
) -> None:
    """Test every ``(category, subtype)`` `_to_proto` emits round-trips back to its class."""
    # Given: a class and its protobuf identity pair.
    # When: the protobuf pair is converted back via `_from_proto`.
    result = electrical_component_class_from_proto(
        cast(_ProtoCategory, category),
        cast(_ProtoSubtype | None, subtype),
    )

    # Then: the original class is recovered.
    assert result is component_class


# ---------------------------------------------------------------------------
# `_from_proto` tests — abstract vs unspecified distinction (the new behaviour)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("category", "abstract_class", "unspecified_class"),
    [
        (
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
            Battery,
            UnspecifiedBattery,
        ),
        (
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER,
            EvCharger,
            UnspecifiedEvCharger,
        ),
        (
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER,
            Inverter,
            UnspecifiedInverter,
        ),
    ],
    ids=["BATTERY", "EV_CHARGER", "INVERTER"],
)
def test_class_from_proto_distinguishes_abstract_from_unspecified(
    category: int,
    abstract_class: type[ElectricalComponent],
    unspecified_class: type[ElectricalComponent],
) -> None:
    """Test that ``None`` resolves to the abstract base and ``...TYPE_UNSPECIFIED`` to Unspecified*.

    This is the behavioural mirror of `_to_proto` distinguishing
    `Battery` → `(BATTERY, None)` from `UnspecifiedBattery` → `(BATTERY, 0)`.
    """
    # Given: a typed family category.
    # When: the category is queried with `subtype=None` then with `...TYPE_UNSPECIFIED`.
    proto_category = cast(_ProtoCategory, category)
    none_result = electrical_component_class_from_proto(proto_category, None)
    unspecified_subtype = cast(
        _ProtoSubtype,
        {
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY: (
                ec_pb2.BATTERY_TYPE_UNSPECIFIED
            ),
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER: (
                ec_pb2.EV_CHARGER_TYPE_UNSPECIFIED
            ),
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER: (
                ec_pb2.INVERTER_TYPE_UNSPECIFIED
            ),
        }[proto_category],
    )
    unspecified_result = electrical_component_class_from_proto(
        proto_category, unspecified_subtype
    )

    # Then: ``None`` returns the abstract base, ``...TYPE_UNSPECIFIED`` returns Unspecified*.
    assert none_result is abstract_class
    assert unspecified_result is unspecified_class
    assert none_result is not unspecified_result


# ---------------------------------------------------------------------------
# `_from_proto` tests — unrecognized handling
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("category", "subtype", "expected_class"),
    [
        (
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_BATTERY,
            999,
            UnrecognizedBattery,
        ),
        (
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_EV_CHARGER,
            999,
            UnrecognizedEvCharger,
        ),
        (
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_INVERTER,
            999,
            UnrecognizedInverter,
        ),
    ],
    ids=["BATTERY", "EV_CHARGER", "INVERTER"],
)
def test_class_from_proto_unknown_subtype_returns_per_family_unrecognized(
    category: int, subtype: int, expected_class: type[ElectricalComponent]
) -> None:
    """Test unknown subtypes in known typed categories return the family `Unrecognized*` class."""
    # Given: a known typed category with an unknown subtype int.
    # When: the protobuf pair is converted to a component class.
    result = electrical_component_class_from_proto(
        cast(_ProtoCategory, category),
        cast(_ProtoSubtype, subtype),
    )

    # Then: the per-family unrecognized class is returned.
    assert result is expected_class


def test_class_from_proto_unknown_category_returns_top_level_unrecognized() -> None:
    """Test unknown categories with no subtype return `UnrecognizedElectricalComponent`."""
    # Given: a category int with no Python class mapping.
    # When: the protobuf pair is converted to a component class.
    result = electrical_component_class_from_proto(cast(_ProtoCategory, 999), None)

    # Then: the top-level unrecognized class is returned.
    assert result is UnrecognizedElectricalComponent


def test_class_from_proto_unknown_category_silently_drops_subtype() -> None:
    """Test unknown categories with a subtype silently drop the subtype int."""
    # Given: a category int with no Python class mapping and a (spurious) subtype int.
    # When: the protobuf pair is converted to a component class.
    result = electrical_component_class_from_proto(
        cast(_ProtoCategory, 999),
        cast(_ProtoSubtype, 5),
    )

    # Then: the top-level unrecognized class is returned (subtype is dropped).
    assert result is UnrecognizedElectricalComponent


# ---------------------------------------------------------------------------
# `_from_proto` rejection cases
# ---------------------------------------------------------------------------


def test_class_from_proto_rejects_typeless_subtype() -> None:
    """Test known typeless categories reject spurious subtype values."""
    # Given: a known typeless category with an impossible subtype.
    # When: the protobuf values are converted to a component class.
    with pytest.raises(UnrecognizedEnumValueError) as exc_info:
        electrical_component_class_from_proto(
            ec_pb2.ELECTRICAL_COMPONENT_CATEGORY_METER,
            cast(_ProtoSubtype, 1),
        )

    # Then: the failing raw protobuf subtype is exposed on the typed error.
    assert exc_info.value.value == 1


# ---------------------------------------------------------------------------
# Coverage tests — every category appears in the conversion table
# ---------------------------------------------------------------------------


def test_every_category_appears_in_to_proto_cases() -> None:
    """Test every protobuf category value is covered by the to-proto cases."""
    # Given: the full set of categories and the categories present in the round-trip cases.
    all_categories = frozenset(ec_pb2.ElectricalComponentCategory.values())
    covered_categories = frozenset(category for _, category, _ in _TO_PROTO_CASES)

    # Then: every category appears at least once in the round-trip cases.
    assert covered_categories == all_categories
