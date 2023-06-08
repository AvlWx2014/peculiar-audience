from collections import namedtuple

import pytest
from hamcrest import assert_that, calling, contains_exactly, contains_inanyorder, equal_to, instance_of, is_, raises

from peculiar_audience import (
    first,
    first_or_none,
    flat_map,
    fold,
    sum_by, flatten, none,
)


@pytest.mark.parametrize(
    "iterable,predicate,expected",
    [
        (range(1, 10), lambda i: i % 2 == 0, 2),
        (range(1, 10), lambda i: i % 3 == 0, 3),
        (range(1, 10), lambda i: i == 10, ValueError()),
    ]
)
def test_first(iterable, predicate, expected):
    if isinstance(expected, Exception):
        assert_that(calling(first).with_args(iterable, predicate), raises(type(expected)))
    else:
        actual = first(iterable, predicate)
        assert_that(actual, equal_to(expected))


@pytest.mark.parametrize(
    "iterable,predicate,expected",
    [
        (range(1, 10), lambda i: i % 2 == 0, 2),
        (range(1, 10), lambda i: i % 3 == 0, 3),
        (range(1, 10), lambda i: i == 10, None),
    ],
)
def test_first_or_none(iterable, predicate, expected):
    actual = first_or_none(iterable, predicate)
    assert_that(actual, equal_to(expected))


def test_flat_map():
    expected = ["0", "2", "4", "6", "8", "1", "3", "5", "7", "9"]
    even = range(0, 10, 2)
    odd = range(1, 10, 2)
    actual = flat_map(even, odd, mapping=str)
    assert_that(actual, contains_exactly(*expected))


def test_flatten():
    expected = range(10)
    even = range(0, 10, 2)
    odd = range(1, 10, 2)
    actual = flatten(even, odd)
    assert_that(actual, contains_inanyorder(*expected))


def test_fold():
    inputs = range(10)
    expected = sum(inputs)
    actual = fold(inputs, 0, lambda x, y: x + y)
    assert_that(actual, equal_to(expected))


@pytest.mark.parametrize(
    "iterable,predicate,expected",
    [
        (range(1, 10), lambda i: i % 10 == 0, True),
        (range(1, 10), lambda i: i % 2 == 0, False),
        (range(1, 10), lambda i: i % 3 == 0, False),
        (range(1, 10), lambda i: i.bit_length() > 4, True)
    ]
)
def test_none(iterable, predicate, expected):
    actual = none(iterable, predicate)
    assert_that(actual, is_(expected))


@pytest.mark.parametrize(
    "iterable,type_,expected",
    [
        (range(10), int, 45),
        (range(10), float, 45.0)
    ]
)
def test_sum_by(iterable, type_, expected):
    # create some temporary objects in order to exercise ``selector``
    T = namedtuple("T", ("value",))
    ts = [T(value=type_(i)) for i in iterable]
    actual = sum_by(ts, lambda o: o.value)
    assert_that(actual, instance_of(type_))
    assert_that(actual, equal_to(expected))
