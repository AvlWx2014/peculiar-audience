from typing import Sequence, Callable, Optional

from ._types import T


__all__ = [
    "last",
    "last_or_none"
]


def last(sequence: Sequence[T], predicate: Callable[[T], bool]) -> T:
    """Return the last item of ``sequence`` matching ``predicate`` or raise if no item matches.

    Raises:
        ValueError: If no item matches ``predicate``.
    """
    for item in sequence[::-1]:
        if predicate(item):
            return item
    raise ValueError("No item found matching predicate.")


def last_or_none(sequence: Sequence[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """Return the last item of ``sequence`` matching ``predicate`` or `None` if no item matches.

    Returns:
        The last item from ``sequence`` that matches ``predicate`` or `None` if no item matches.
    """
    try:
        result = last(sequence, predicate)
    except ValueError:
        result = None

    return result
