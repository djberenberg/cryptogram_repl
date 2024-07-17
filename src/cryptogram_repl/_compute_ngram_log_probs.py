import collections
import itertools
import math
import string
from collections import Counter
from typing import Iterable, TypeVar

T = TypeVar("T")

CHAR_SET = set(string.ascii_uppercase)


def _sliding_window(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def compute_ngram_log_probs(iterator: Iterable[str], n: int) -> dict[str, float]:
    ngram_counts = Counter(
        itertools.filterfalse(
            lambda x: set(x) - CHAR_SET,
            map(
                "".join,
                itertools.chain.from_iterable(
                    _sliding_window(x, n) for x in map(lambda x: x.casefold().upper(), iterator)
                ),
            ),
        )
    )

    total_counts = ngram_counts.total()
    return {k: math.log(count / total_counts) for k, count in ngram_counts.items()}
