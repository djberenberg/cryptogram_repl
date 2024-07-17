import itertools
import math
import string
from collections import Counter
from typing import Iterable

from ._sliding_window import sliding_window

CHAR_SET = set(string.ascii_uppercase)


def compute_ngram_log_probs(iterator: Iterable[str], n: int) -> dict[str, float]:
    ngram_counts = Counter(
        itertools.filterfalse(
            lambda x: set(x) - CHAR_SET,
            map(
                "".join,
                itertools.chain.from_iterable(
                    sliding_window(x, n) for x in map(lambda x: x.casefold().upper(), iterator)
                ),
            ),
        )
    )

    total_counts = ngram_counts.total()
    return {k: math.log(count / total_counts) for k, count in ngram_counts.items()}
