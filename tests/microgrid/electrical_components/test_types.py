# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Tests for the electrical component type aliases."""

from typing import get_args

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
    ElectricalComponentTypes,
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
    ProblematicElectricalComponentTypes,
    PvInverter,
    StaticTransferSwitch,
    SteamBoiler,
    UninterruptiblePowerSupply,
    UnrecognizedBattery,
    UnrecognizedElectricalComponent,
    UnrecognizedElectricalComponentTypes,
    UnrecognizedEvCharger,
    UnrecognizedInverter,
    UnspecifiedBattery,
    UnspecifiedElectricalComponent,
    UnspecifiedElectricalComponentTypes,
    UnspecifiedEvCharger,
    UnspecifiedInverter,
    WindTurbine,
)

_EXPECTED_ELECTRICAL_COMPONENT_TYPES = frozenset(
    {
        Breaker,
        CapacitorBank,
        Chp,
        Converter,
        CryptoMiner,
        Electrolyzer,
        GridConnectionPoint,
        Hvac,
        Meter,
        MismatchedCategoryElectricalComponent,
        Plc,
        PowerTransformer,
        Precharger,
        StaticTransferSwitch,
        SteamBoiler,
        UninterruptiblePowerSupply,
        UnrecognizedElectricalComponent,
        UnspecifiedElectricalComponent,
        WindTurbine,
        LiIonBattery,
        NaIonBattery,
        UnrecognizedBattery,
        UnspecifiedBattery,
        AcEvCharger,
        DcEvCharger,
        HybridEvCharger,
        UnrecognizedEvCharger,
        UnspecifiedEvCharger,
        BatteryInverter,
        HybridInverter,
        PvInverter,
        UnrecognizedInverter,
        UnspecifiedInverter,
    }
)
"""The concrete typed-family classes (batteries, EV chargers, inverters)."""

_EXPECTED_ABSTRACT_BASES = frozenset({Battery, EvCharger, Inverter})
"""The abstract typed family bases — never members of `ElectricalComponentTypes`."""

_EXPECTED_UNSPECIFIED_TYPES = frozenset(
    {
        UnspecifiedBattery,
        UnspecifiedElectricalComponent,
        UnspecifiedEvCharger,
        UnspecifiedInverter,
    }
)
"""The unspecified concrete markers (`Unspecified*`)."""

# The tuple annotation is needed to work around a mypy quirk: when joining
# class objects with different constructor signatures (`type: int` vs
# `category: int`), mypy joins them as callables and rejects the set literal.
_UNRECOGNIZED_CLASSES: tuple[type[object], ...] = (
    UnrecognizedBattery,
    UnrecognizedElectricalComponent,
    UnrecognizedEvCharger,
    UnrecognizedInverter,
)

_EXPECTED_UNRECOGNIZED_TYPES = frozenset(_UNRECOGNIZED_CLASSES)
"""The unrecognized concrete markers (`Unrecognized*`)."""

_EXPECTED_PROBLEMATIC_TYPES = (
    _EXPECTED_UNSPECIFIED_TYPES
    | _EXPECTED_UNRECOGNIZED_TYPES
    | {MismatchedCategoryElectricalComponent}
)
"""All problem markers (unspecified, unrecognized and mismatched)."""


def test_electrical_component_types_unions_simple_and_typed() -> None:
    """Test `ElectricalComponentTypes` is exactly the simple set ∪ the typed-family classes."""
    members = frozenset(get_args(ElectricalComponentTypes))
    assert members == _EXPECTED_ELECTRICAL_COMPONENT_TYPES


def test_electrical_component_types_exclude_abstract_bases() -> None:
    """Test that the abstract typed bases never appear in `ElectricalComponentTypes`."""
    members = frozenset(get_args(ElectricalComponentTypes))
    assert members.isdisjoint(_EXPECTED_ABSTRACT_BASES)


def test_unspecified_alias_matches_expected_set() -> None:
    """Test that `UnspecifiedElectricalComponentTypes` matches the expected set."""
    assert (
        frozenset(get_args(UnspecifiedElectricalComponentTypes))
        == _EXPECTED_UNSPECIFIED_TYPES
    )


def test_unrecognized_alias_matches_expected_set() -> None:
    """Test that `UnrecognizedElectricalComponentTypes` matches the expected set."""
    assert (
        frozenset(get_args(UnrecognizedElectricalComponentTypes))
        == _EXPECTED_UNRECOGNIZED_TYPES
    )


def test_problematic_alias_unions_all_problem_markers() -> None:
    """Test `ProblematicElectricalComponentTypes` is the union of every problem marker.

    The alias collapses through `UnspecifiedElectricalComponentTypes` and
    `UnrecognizedElectricalComponentTypes` and adds
    `MismatchedCategoryElectricalComponent` on top — so collecting `get_args`
    transitively must equal the full problem-marker set.
    """
    args = get_args(ProblematicElectricalComponentTypes)
    flattened: set[type[object]] = set()
    for arg in args:
        nested = get_args(arg)
        if nested:
            flattened.update(nested)
        else:
            flattened.add(arg)
    assert flattened == _EXPECTED_PROBLEMATIC_TYPES
