"""Functional-esque tools for Python inspired by the Kotlin Collections API."""

from typing import Callable, Iterable, List, Optional, overload

from ._types import T, R

__all__ = [
    "first",
    "first_or_none",
    "flat_map",
    "flatten",
    "fold",
    "none",
    "sum_by"
]


def first(iterable: Iterable[T], predicate: Callable[[T], bool]) -> T:
    """Return the first item of ``collection`` matching ``predicate`` or raise if no item matches.

    Raises:
        ValueError: If no item matches ``predicate``.
    """
    for item in iterable:
        if predicate(item):
            return item
    raise ValueError("No item found matching predicate.")


def first_or_none(iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """
    Return the first item of ``collection`` matching ``predicate`` or `None` if no item matches.
    """
    try:
        result = first(iterable, predicate)
    except ValueError:
        result = None

    return result


def flat_map(*iterables: Iterable[T], mapping: Callable[[T], R]) -> List[R]:
    """Flatten ``iterables`` in to a single list comprising transformed items from each iterable.

    Items from each iterable in ``iterables`` are transformed according to ``mapping``.
    """
    # use built-in `map` to avoid allocating a list for each `map` operation
    return [item for iterable in iterables for item in map(mapping, iterable)]


def flatten(*iterables: Iterable[T]) -> List[T]:
    """Flatten ``iterables`` in to a single list comprising all items from all iterables."""
    return [item for iterable in iterables for item in iterable]


def fold(
    iterable: Iterable[T], initial_value: R, accumulator: Callable[[R, T], R]
) -> R:
    """Accumulates value starting from ``initial_value``.

    Accumulation starts from ``initial_value`` and applies ``accumulator`` from left
    to right across ``iterable`` passing the current accumulated value with each item.
    """
    acc = initial_value
    for item in iterable:
        acc = accumulator(acc, item)
    return acc


def none(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """Returns ``True`` if no item in iterable matches ``predicate`` and ``False`` otherwise."""
    for item in iterable:
        if predicate(item):
            return False
    return True


@overload
def sum_by(iterable: Iterable[T], selector: Callable[[T], int]) -> int: ...
@overload
def sum_by(iterable: Iterable[T], selector: Callable[[T], float]) -> float: ...
# Type hints intentionally left out of the signature since @overload is being used
def sum_by(iterable, selector):
    """Accumulate a sum of each item in ``iterable``.

    ``selector`` maps each item in ``iterable`` to a numeric value to add.

    If ``selector`` returns an :py:obj:`int` for each value, then the return value
    will be an :py:obj:`int`. Otherwise if ``selector`` returns a :py:obj:`float` then
    the return value will be a :py:obj:`float`.
    """
    sum_ = 0
    for item in iterable:
        sum_ += selector(item)
    return sum_
