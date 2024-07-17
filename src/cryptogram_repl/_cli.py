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

from ._compute_ngram_log_probs import compute_ngram_log_probs
from ._cryptogram_repl import CryptogramREPL


def cli():

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers()
    parser_repl = subparsers.add_parser("repl", help=__doc__)
    parser_repl.set_defaults(command="repl")

    parser_repl.add_argument(
        "puzzle_file", type=str, help="Input puzzle as a single-line text file."
    )

    parser_ngrams = subparsers.add_parser(
        "compute-logprobs", help="Compute n-gram log-probabilities"
    )

    parser_ngrams.set_defaults(command="logprobs")
    parser_ngrams.add_argument("input_txt_file", type=str, help="Text file to calibrate log probs.")
    parser_ngrams.add_argument("-n", type=int, default=4, help="Window size")

    args = parser.parse_args()

    args = parser.parse_args()

    match args.command:
        case "repl":
            with open(args.puzzle_file, "r") as f:
                puzzle = f.read().strip()

            CryptogramREPL(puzzle).run()

        case "logprobs":

            with open(args.input_txt_file, "r") as f:
                ngram_logprobs = compute_ngram_log_probs(f, args.n)
                for ngram in sorted(ngram_logprobs):
                    print(f"{ngram} {ngram_logprobs[ngram]}")
