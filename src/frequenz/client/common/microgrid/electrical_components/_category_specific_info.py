# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Category specific info carried by an electrical component."""

import dataclasses
from collections.abc import Mapping
from typing import Any


@dataclasses.dataclass(frozen=True, kw_only=True)
class CategorySpecificInfo:
    """The category specific info carried by an electrical component.

    A protobuf electrical component may carry a `category_specific_info` variant
    with extra fields tied to its category. Fields this library version
    understands are translated into typed attributes on the concrete component
    (e.g. the battery type). Anything left over — either because the component's
    category is not recognized, or because a newer API version added fields this
    client doesn't know yet — is preserved here so callers can still inspect the
    raw values.
    """

    kind: str
    """The name of the info variant carried on the wire (e.g. `"battery"`)."""

    fields: Mapping[str, Any] = dataclasses.field(
        default_factory=dict,
        # Excluded from the hash: values may be unhashable (e.g. lists), and even
        # repr()-folding them breaks the eq/hash invariant since values that
        # compare equal can differ under repr()/hash() (e.g. 1 == 1.0 == True).
        # Instances hash on `kind` alone, mirroring `metric_config_bounds`.
        hash=False,
    )
    """The leftover fields not translated into typed attributes.

    The keys are the protobuf field names and the values their decoded content.
    """
