# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Pagination information used by common clients."""

from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True, kw_only=True)
class BasePaginationInfo:
    """A base class for well-formed and malformed pagination information.

    This class cannot be instantiated directly. Use
    [`PaginationInfo`][..PaginationInfo] for well-formed pagination
    information or [`InvalidPaginationInfo`][..InvalidPaginationInfo] to
    preserve malformed wire data.
    """

    total_items: int
    """The total number of items that match the request."""

    next_page_token: str | None = None
    """The token identifying the next page of results.

    If `None`, the server did not send a token, so there are no more pages.
    """

    # pylint: disable-next=unused-argument
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Prevent instantiation of this class."""
        if cls is BasePaginationInfo:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")
        return super().__new__(cls)


@dataclass(frozen=True, kw_only=True)
class PaginationInfo(BasePaginationInfo):
    """Information about the pagination of a list request.

    The [`total_items`][.total_items] count is a number of items, so it can
    never be negative. Pagination information built from a wire message that
    breaks this rule is an
    [`InvalidPaginationInfo`][..InvalidPaginationInfo] instead, so code
    holding a `PaginationInfo` can use the count in arithmetic without
    checking it first.

    Note:
        Raises a `ValueError` if [`total_items`][.total_items] is negative.
        Use [`InvalidPaginationInfo`][..InvalidPaginationInfo] to represent
        malformed pagination data received from the wire.
    """

    def __post_init__(self) -> None:
        """Validate pagination information.

        Raises:
            ValueError: If [`total_items`][..total_items] is negative.
        """
        if self.total_items < 0:
            raise ValueError(
                f"total_items must be non-negative, not {self.total_items}"
            )

    def __str__(self) -> str:
        """Return a compact string representation of this pagination information."""
        return f"items={self.total_items},next={self.next_page_token}"


@dataclass(frozen=True, kw_only=True)
class InvalidPaginationInfo(BasePaginationInfo):
    """Pagination information with malformed data received from the wire.

    This class preserves pagination data that fails the invariants required
    for a well-formed [`PaginationInfo`][..PaginationInfo], allowing callers
    to inspect the raw values without accidentally using them as a count.

    This class does not enforce any invariants on construction.
    """

    def __str__(self) -> str:
        """Return a compact string representation of this invalid pagination info."""
        total_items = (
            f"<invalid:{self.total_items}>"
            if self.total_items < 0
            else str(self.total_items)
        )
        return f"items={total_items},next={self.next_page_token}"
