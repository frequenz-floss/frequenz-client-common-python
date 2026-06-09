# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Pagination information used by common clients."""

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class PaginationInfo:
    """Information about the pagination of a list request."""

    total_items: int
    """The total number of items that match the request."""

    next_page_token: str | None = None
    """The token identifying the next page of results."""
