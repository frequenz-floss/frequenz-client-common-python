# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Crypto miner electrical component."""

import dataclasses

from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class CryptoMiner(ElectricalComponent):
    """A crypto miner electrical component."""

    _category: int = dataclasses.field(
        default=14, repr=False
    )  # ElectricalComponentCategory.CRYPTO_MINER
    """The category of this electrical component."""
