# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Crypto miner electrical component."""

import dataclasses
from typing import Literal

from ._category import ComponentCategory
from ._electrical_component import ElectricalComponent


@dataclasses.dataclass(frozen=True, kw_only=True)
class CryptoMiner(ElectricalComponent):
    """A crypto miner electrical component."""

    category: Literal[ComponentCategory.CRYPTO_MINER] = ComponentCategory.CRYPTO_MINER
    """The category of this electrical component."""
