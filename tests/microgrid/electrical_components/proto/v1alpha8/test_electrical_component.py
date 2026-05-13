# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Tests for electrical component enum to/from protobuf v1alpha8 conversion.

These tests ensure that, for this version, all enum members are correctly matched by
name and value between the Python electrical component enums and the corresponding
protobuf enums.
"""

from typing import TypeAlias

import pytest
from frequenz.api.common.v1alpha8.microgrid.electrical_components import (
    electrical_components_pb2,
)

from frequenz.client.common.microgrid.electrical_components import (
    ElectricalComponentCategory,
    ElectricalComponentDiagnosticCode,
    ElectricalComponentStateCode,
)
from frequenz.client.common.microgrid.electrical_components.proto.v1alpha8 import (
    electrical_component_category_from_proto,
    electrical_component_category_to_proto,
    electrical_component_diagnostic_code_from_proto,
    electrical_component_diagnostic_code_to_proto,
    electrical_component_state_code_from_proto,
    electrical_component_state_code_to_proto,
)

CATEGORY_PB_NAMES: list[str] = [
    m.name
    for m in electrical_components_pb2.ElectricalComponentCategory.DESCRIPTOR.values
]
CategoryValue: TypeAlias = (
    electrical_components_pb2.ElectricalComponentCategory.ValueType
)
STATE_CODE_PB_NAMES: list[str] = [
    m.name
    for m in electrical_components_pb2.ElectricalComponentStateCode.DESCRIPTOR.values
]
StateCodeValue: TypeAlias = (
    electrical_components_pb2.ElectricalComponentStateCode.ValueType
)
DIAGNOSTIC_CODE_PB_NAMES: list[str] = [
    m.name
    for m in electrical_components_pb2.ElectricalComponentDiagnosticCode.DESCRIPTOR.values
]
DiagnosticCodeValue: TypeAlias = (
    electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType
)

UNKNOWN_CATEGORY_PB_VALUE = (
    electrical_components_pb2.ElectricalComponentCategory.ValueType(
        max(m.value for m in ElectricalComponentCategory) + 1
    )
)
UNKNOWN_STATE_CODE_PB_VALUE = (
    electrical_components_pb2.ElectricalComponentStateCode.ValueType(
        max(m.value for m in ElectricalComponentStateCode) + 1
    )
)
UNKNOWN_DIAGNOSTIC_CODE_PB_VALUE = (
    electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType(
        max(m.value for m in ElectricalComponentDiagnosticCode) + 1
    )
)


def test_category_no_implicit_to_proto_conversion() -> None:
    """Test that protobuf category values are not implicitly convertible."""
    # mypy should complain about this assignment, so we ignore the type check here.
    # If mypy doesn't find an issue with this conversion, it should complain about
    # the ignore comment having no effect.
    category = list(ElectricalComponentCategory)[0]
    _: CategoryValue = category.value  # type: ignore[assignment]
    electrical_components_pb2.ElectricalComponentCategory.Name(
        category.value  # type: ignore[arg-type]
    )


@pytest.mark.parametrize("pb_name", CATEGORY_PB_NAMES)
def test_category_proto_enum_matches_enum_name(pb_name: str) -> None:
    """Test that all known protobuf category names have a matching enum member."""
    pb_value = electrical_components_pb2.ElectricalComponentCategory.Value(pb_name)
    try:
        category = ElectricalComponentCategory[
            pb_name.removeprefix("ELECTRICAL_COMPONENT_CATEGORY_")
        ]
        assert category.value == pb_value
    except KeyError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize("pb_name", CATEGORY_PB_NAMES)
def test_category_proto_enum_matches_enum_value(pb_name: str) -> None:
    """Test that all known protobuf category values have a matching enum member."""
    pb_value = electrical_components_pb2.ElectricalComponentCategory.Value(pb_name)
    try:
        category = ElectricalComponentCategory(pb_value)
        assert category.value == pb_value
    except ValueError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize(
    "category", list(ElectricalComponentCategory), ids=lambda m: m.name
)
def test_category_enum_matches_proto_enum_name(
    category: ElectricalComponentCategory,
) -> None:
    """Test that all category enum members have a matching protobuf enum name."""
    pb_value = electrical_components_pb2.ElectricalComponentCategory.ValueType(
        category.value
    )
    pb_name = electrical_components_pb2.ElectricalComponentCategory.Name(pb_value)
    assert pb_name == f"ELECTRICAL_COMPONENT_CATEGORY_{category.name}"


@pytest.mark.parametrize(
    "category", list(ElectricalComponentCategory), ids=lambda m: m.name
)
def test_category_enum_matches_proto_enum_value(
    category: ElectricalComponentCategory,
) -> None:
    """Test that all category enum members have a matching protobuf enum value."""
    pb_value = electrical_components_pb2.ElectricalComponentCategory.Value(
        f"ELECTRICAL_COMPONENT_CATEGORY_{category.name}"
    )
    assert category.value == pb_value


@pytest.mark.parametrize("pb_name", CATEGORY_PB_NAMES)
def test_category_from_proto(pb_name: str) -> None:
    """Test category conversion from protobuf returns a matching member or int."""
    pb_value = electrical_components_pb2.ElectricalComponentCategory.Value(pb_name)
    category = electrical_component_category_from_proto(pb_value)
    if pb_value in [m.value for m in ElectricalComponentCategory]:
        assert category is ElectricalComponentCategory(pb_value)
    else:
        assert category == pb_value


def test_category_from_proto_unknown() -> None:
    """Test category conversion from protobuf for unknown values returns the int."""
    category = electrical_component_category_from_proto(UNKNOWN_CATEGORY_PB_VALUE)
    assert isinstance(category, int)
    assert category == UNKNOWN_CATEGORY_PB_VALUE


@pytest.mark.parametrize(
    "category", list(ElectricalComponentCategory), ids=lambda m: m.name
)
def test_category_to_proto(category: ElectricalComponentCategory) -> None:
    """Test category conversion to protobuf returns a matching protobuf value."""
    pb_value = electrical_component_category_to_proto(category)
    assert pb_value == category.value


def test_state_code_no_implicit_to_proto_conversion() -> None:
    """Test that protobuf state code values are not implicitly convertible."""
    # mypy should complain about this assignment, so we ignore the type check here.
    # If mypy doesn't find an issue with this conversion, it should complain about
    # the ignore comment having no effect.
    state_code = list(ElectricalComponentStateCode)[0]
    _: StateCodeValue = state_code.value  # type: ignore[assignment]
    electrical_components_pb2.ElectricalComponentStateCode.Name(
        state_code.value  # type: ignore[arg-type]
    )


@pytest.mark.parametrize("pb_name", STATE_CODE_PB_NAMES)
def test_state_code_proto_enum_matches_enum_name(pb_name: str) -> None:
    """Test that all known protobuf state code names have a matching enum member."""
    pb_value = electrical_components_pb2.ElectricalComponentStateCode.Value(pb_name)
    try:
        state_code = ElectricalComponentStateCode[
            pb_name.removeprefix("ELECTRICAL_COMPONENT_STATE_CODE_")
        ]
        assert state_code.value == pb_value
    except KeyError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize("pb_name", STATE_CODE_PB_NAMES)
def test_state_code_proto_enum_matches_enum_value(pb_name: str) -> None:
    """Test that all known protobuf state code values have a matching enum member."""
    pb_value = electrical_components_pb2.ElectricalComponentStateCode.Value(pb_name)
    try:
        state_code = ElectricalComponentStateCode(pb_value)
        assert state_code.value == pb_value
    except ValueError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize(
    "state_code", list(ElectricalComponentStateCode), ids=lambda m: m.name
)
def test_state_code_enum_matches_proto_enum_name(
    state_code: ElectricalComponentStateCode,
) -> None:
    """Test that all state code enum members have a matching protobuf enum name."""
    pb_value = electrical_components_pb2.ElectricalComponentStateCode.ValueType(
        state_code.value
    )
    pb_name = electrical_components_pb2.ElectricalComponentStateCode.Name(pb_value)
    assert pb_name == f"ELECTRICAL_COMPONENT_STATE_CODE_{state_code.name}"


@pytest.mark.parametrize(
    "state_code", list(ElectricalComponentStateCode), ids=lambda m: m.name
)
def test_state_code_enum_matches_proto_enum_value(
    state_code: ElectricalComponentStateCode,
) -> None:
    """Test that all state code enum members have a matching protobuf enum value."""
    pb_value = electrical_components_pb2.ElectricalComponentStateCode.Value(
        f"ELECTRICAL_COMPONENT_STATE_CODE_{state_code.name}"
    )
    assert state_code.value == pb_value


@pytest.mark.parametrize("pb_name", STATE_CODE_PB_NAMES)
def test_state_code_from_proto(pb_name: str) -> None:
    """Test state code conversion from protobuf returns a matching member or int."""
    pb_value = electrical_components_pb2.ElectricalComponentStateCode.Value(pb_name)
    state_code = electrical_component_state_code_from_proto(pb_value)
    if pb_value in [m.value for m in ElectricalComponentStateCode]:
        assert state_code is ElectricalComponentStateCode(pb_value)
    else:
        assert state_code == pb_value


def test_state_code_from_proto_unknown() -> None:
    """Test state code conversion from protobuf for unknown values returns the int."""
    state_code = electrical_component_state_code_from_proto(UNKNOWN_STATE_CODE_PB_VALUE)
    assert isinstance(state_code, int)
    assert state_code == UNKNOWN_STATE_CODE_PB_VALUE


@pytest.mark.parametrize(
    "state_code", list(ElectricalComponentStateCode), ids=lambda m: m.name
)
def test_state_code_to_proto(state_code: ElectricalComponentStateCode) -> None:
    """Test state code conversion to protobuf returns a matching protobuf value."""
    pb_value = electrical_component_state_code_to_proto(state_code)
    assert pb_value == state_code.value


def test_diagnostic_code_no_implicit_to_proto_conversion() -> None:
    """Test that protobuf diagnostic code values are not implicitly convertible."""
    # mypy should complain about this assignment, so we ignore the type check here.
    # If mypy doesn't find an issue with this conversion, it should complain about
    # the ignore comment having no effect.
    diagnostic_code = list(ElectricalComponentDiagnosticCode)[0]
    _: DiagnosticCodeValue = diagnostic_code.value  # type: ignore[assignment]
    electrical_components_pb2.ElectricalComponentDiagnosticCode.Name(
        diagnostic_code.value  # type: ignore[arg-type]
    )


@pytest.mark.parametrize("pb_name", DIAGNOSTIC_CODE_PB_NAMES)
def test_diagnostic_code_proto_enum_matches_enum_name(pb_name: str) -> None:
    """Test that all known protobuf diagnostic code names have a matching member."""
    pb_value = electrical_components_pb2.ElectricalComponentDiagnosticCode.Value(
        pb_name
    )
    try:
        diagnostic_code = ElectricalComponentDiagnosticCode[
            pb_name.removeprefix("ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_")
        ]
        assert diagnostic_code.value == pb_value
    except KeyError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize("pb_name", DIAGNOSTIC_CODE_PB_NAMES)
def test_diagnostic_code_proto_enum_matches_enum_value(pb_name: str) -> None:
    """Test that all known protobuf diagnostic code values have a matching member."""
    pb_value = electrical_components_pb2.ElectricalComponentDiagnosticCode.Value(
        pb_name
    )
    try:
        diagnostic_code = ElectricalComponentDiagnosticCode(pb_value)
        assert diagnostic_code.value == pb_value
    except ValueError:
        pass  # It is OK to have new protobuf enum values not yet in the enum.


@pytest.mark.parametrize(
    "diagnostic_code", list(ElectricalComponentDiagnosticCode), ids=lambda m: m.name
)
def test_diagnostic_code_enum_matches_proto_enum_name(
    diagnostic_code: ElectricalComponentDiagnosticCode,
) -> None:
    """Test that all diagnostic code enum members have a matching protobuf name."""
    pb_value = electrical_components_pb2.ElectricalComponentDiagnosticCode.ValueType(
        diagnostic_code.value
    )
    pb_name = electrical_components_pb2.ElectricalComponentDiagnosticCode.Name(pb_value)
    assert pb_name == f"ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_{diagnostic_code.name}"


@pytest.mark.parametrize(
    "diagnostic_code", list(ElectricalComponentDiagnosticCode), ids=lambda m: m.name
)
def test_diagnostic_code_enum_matches_proto_enum_value(
    diagnostic_code: ElectricalComponentDiagnosticCode,
) -> None:
    """Test that all diagnostic code enum members have a matching protobuf value."""
    pb_value = electrical_components_pb2.ElectricalComponentDiagnosticCode.Value(
        f"ELECTRICAL_COMPONENT_DIAGNOSTIC_CODE_{diagnostic_code.name}"
    )
    assert diagnostic_code.value == pb_value


@pytest.mark.parametrize("pb_name", DIAGNOSTIC_CODE_PB_NAMES)
def test_diagnostic_code_from_proto(pb_name: str) -> None:
    """Test diagnostic code conversion from protobuf returns a matching member or int."""
    pb_value = electrical_components_pb2.ElectricalComponentDiagnosticCode.Value(
        pb_name
    )
    diagnostic_code = electrical_component_diagnostic_code_from_proto(pb_value)
    if pb_value in [m.value for m in ElectricalComponentDiagnosticCode]:
        assert diagnostic_code is ElectricalComponentDiagnosticCode(pb_value)
    else:
        assert diagnostic_code == pb_value


def test_diagnostic_code_from_proto_unknown() -> None:
    """Test diagnostic code conversion from protobuf for unknown values returns the int."""
    diagnostic_code = electrical_component_diagnostic_code_from_proto(
        UNKNOWN_DIAGNOSTIC_CODE_PB_VALUE
    )
    assert isinstance(diagnostic_code, int)
    assert diagnostic_code == UNKNOWN_DIAGNOSTIC_CODE_PB_VALUE


@pytest.mark.parametrize(
    "diagnostic_code", list(ElectricalComponentDiagnosticCode), ids=lambda m: m.name
)
def test_diagnostic_code_to_proto(
    diagnostic_code: ElectricalComponentDiagnosticCode,
) -> None:
    """Test diagnostic code conversion to protobuf returns a matching value."""
    pb_value = electrical_component_diagnostic_code_to_proto(diagnostic_code)
    assert pb_value == diagnostic_code.value
