import pytest as pytest
from hamcrest import assert_that, contains_exactly, is_

from peculiar_audience.shadow import all, any, map, __pyall, __pyany, __pymap


@pytest.mark.parametrize(
    "iterable,predicate,expected",
    [
        (range(1, 10), lambda i: i % 10 == 0, False),
        (range(1, 10), lambda i: i % 2 == 0, False),
        (range(1, 10), lambda i: i % 3 == 0, False),
        (range(1, 10), lambda i: i.bit_length() <= 4, True),
        (range(1, 10), lambda i: i < 10, True),
    ]
)
def test_all(iterable, predicate, expected):
    compat = __pyall(__pymap(predicate, iterable))
    actual = all(iterable, predicate)
    assert_that(actual, is_(expected))
    assert_that(actual, is_(compat))


@pytest.mark.parametrize(
    "iterable,predicate,expected",
    [
        (range(1, 10), lambda i: i % 10 == 0, False),
        (range(1, 10), lambda i: i % 2 == 0, True),
        (range(1, 10), lambda i: i % 3 == 0, True),
        (range(1, 10), lambda i: i.bit_length() <= 4, True),
    ]
)
def test_any(iterable, predicate, expected):
    compat = __pyany(__pymap(predicate, iterable))
    actual = any(iterable, predicate)
    assert_that(actual, is_(expected))
    assert_that(actual, is_(compat))


def test_map():
    iterable = "abcdefghijklmnopqrstuvwxyz"
    expected = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    compat = __pymap(str.upper, iterable)
    actual = map(iterable, str.upper)
    assert_that(actual, contains_exactly(*expected))
    assert_that(actual, contains_exactly(*compat))
