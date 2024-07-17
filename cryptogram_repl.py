"""
Solve NYT cryptograms interactively!


You have 3 commands:

### `substitute STRING1 STRING2`
Add entries to your cipher. Accepts two same-length capitalized strings. (e.g., `substitute ABCD EFGH`).
Other aliases: `sub`, `s`.

### `revert STRING`
Revert a set of characters back so they map to themselves in the cipher (e.g., `revert ABCDEF`. 
Other aliases: `rev`, `r`.

### `export`

Export the cipher you've created.
"""

import argparse
import textwrap
import sys
from io import StringIO
from dataclasses import dataclass, field

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


PROMPT = f"Enter a command ({bcolors.FAIL}substitute{bcolors.ENDC}, {bcolors.OKGREEN}revert{bcolors.ENDC}, or {bcolors.OKBLUE}export{bcolors.ENDC}) "
PUZZLE_PRFX = f"{bcolors.FAIL}{bcolors.BOLD}{'Puzzle':<10s}{bcolors.ENDC}"
SOLN_PRFX = f"{bcolors.HEADER}{bcolors.BOLD}{'Solution':<10s}{bcolors.ENDC}"

SOURCE = f"{bcolors.BOLD}{bcolors.UNDERLINE}Source{bcolors.ENDC}"
TARGET = f"{bcolors.BOLD}{bcolors.UNDERLINE}Target{bcolors.ENDC}" 


@dataclass
class CryptogramREPL:

    start_puzzle: str
    cipher: dict[str, str] = field(init=False)


    def __post_init__(self):
        self.cipher = {char: char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

    
    @property
    def _back_cipher(self) -> dict[str, str]:
        return {v: k for k, v in self.cipher.items()}

    def apply_cipher(self, string: str) -> str:
        
        return "".join(self.cipher[c] if c in self.cipher else c for c in string)
        
    
    def substitute(self, args: list[str]):
        if len(args) < 2:
            raise ValueError("Substitute: Not enough args!")

        from_letters, to_letters, *_ = args

        if len(from_letters) != len(to_letters):
            raise ValueError("Substitute: Not the same length for substitution")



        for f, t in zip(from_letters, to_letters):
        
            if f not in self.cipher or t not in self.cipher:
                raise ValueError(f"Substitute: Bad substitution {f} -> {t}")

        for f, t in zip(from_letters, to_letters):
            self.cipher[f] = t


    def revert(self, letters: str):
        for letter in letters:
            if letter not in self.cipher:
                raise ValueError(f"Nothing valid to revert")
    
        for letter in letters:
            self.cipher[letter] = letter

    def export(self):

        print(f"{SOURCE:<7s} --> {TARGET:<7s}")
        for s, t in self.cipher.items():
            if s != t:
                print(f"{bcolors.BOLD}{bcolors.FAIL}{s:<7s}{bcolors.ENDC} --> {bcolors.BOLD}{bcolors.OKBLUE}{t}{bcolors.ENDC}")
            else:
                print(f"{s:<7s} --> {t:<7s}")

    def quit(self):

        print("Quitting")
        sys.exit(0)
    
    def process_command(self, input_command: str):

        if not input_command:
            raise ValueError("No command provided")
        
        command, *args = input_command.split(" ")

        match command:
            case "substitute" | "sub" | "s":
                self.substitute(args)
                
            case "revert" | "rev" | "r":
                self.revert(args)

            case "export" | "x":
                self.export()

            case "quit" | "q":
                self.quit()


    def print(self):
        
        current_solution = self.apply_cipher(self.start_puzzle)
        puzzle_lines = textwrap.wrap(self.start_puzzle, width=110)
        solution_lines = textwrap.wrap(current_solution, width=110)


        for i, (puzz, soln) in enumerate(zip(puzzle_lines, solution_lines)):
            soln_line = StringIO()
            for p, s in zip(puzz, soln):
                if p == s:
                    soln_line.write(s)
                else:
                    soln_line.write(f"{bcolors.UNDERLINE}{bcolors.OKGREEN}{s}{bcolors.ENDC}")

            print(f"{PUZZLE_PRFX}: {puzz}")
            print(f"{SOLN_PRFX}: {soln_line.getvalue()}")

    def run(self):

        try:
            while True:
                self.print()
                try:
                    self.process_command(input(PROMPT))
                except ValueError as e:
                    print(f"{bcolors.FAIL}{bcolors.BOLD}{e}{bcolors.ENDC}")
                    continue

        except KeyboardInterrupt:
            print("Quitting")
            sys.exit(0)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("puzzle_file", type=str, help="Input puzzle as a single-line text file.")

    args = parser.parse_args()

    with open(args.puzzle_file, "r") as f:
        puzzle = f.read().strip()

    CryptogramREPL(puzzle).run()

