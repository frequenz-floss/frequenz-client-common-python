# License: MIT
# Copyright © 2025 Frequenz Energy-as-a-Service GmbH

"""Show Protobuf version warning during tests, but don't treat as error."""

import warnings

warnings.filterwarnings(
    "once",
    message=r"Protobuf gencode version 5\..*exactly one major version older.*",
    category=UserWarning,
)
