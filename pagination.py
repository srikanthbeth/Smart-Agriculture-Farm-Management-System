from typing import Optional


def calculate_offset(
    page: int,
    limit: int
) -> int:
    """
    Calculate SQL offset from page and limit.
    """

    return (page - 1) * limit


def validate_pagination(
    page: int,
    limit: int
):
    """
    Validate pagination parameters.
    """

    if page < 1:
        raise ValueError(
            "Page must be greater than 0"
        )

    if limit < 1:
        raise ValueError(
            "Limit must be greater than 0"
        )

    if limit > 100:
        raise ValueError(
            "Limit cannot exceed 100"
        )


def validate_sort_order(
    sort_order: str
) -> str:

    sort_order = sort_order.lower()

    if sort_order not in {
        "asc",
        "desc"
    }:
        raise ValueError(
            "sort_order must be either 'asc' or 'desc'"
        )

    return sort_order