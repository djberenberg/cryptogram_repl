"""
Solve NYT cryptograms interactively!

You have 3 commands:

### `substitute STRING1 STRING2`
Add entries to your cipher. Accepts two same-length capitalized strings. (e.g., `sub ABCD EFGH`).
Other aliases: `sub`, `s`.

### `revert STRING`
Revert a set of characters back so they map to themselves in the cipher (e.g., `revert ABCDEF`.
Other aliases: `rev`, `r`.

### `export`
Export the cipher you've created.
"""

import argparse

from ._cryptogram_repl import CryptogramREPL


def cli():

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("puzzle_file", type=str, help="Input puzzle as a single-line text file.")

    args = parser.parse_args()

    with open(args.puzzle_file, "r") as f:
        puzzle = f.read().strip()

    CryptogramREPL(puzzle).run()
