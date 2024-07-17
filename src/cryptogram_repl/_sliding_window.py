import collections
import itertools
from typing import Iterable, TypeVar

T = TypeVar("T")


def sliding_window(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)
