import sys
import textwrap
from dataclasses import dataclass, field
from io import StringIO

from ._color_enum import ColorEnum
from ._color_text import color_text

SUB = color_text("substitute", ColorEnum.OKGREEN)
REV = color_text("revert", ColorEnum.FAIL)
EXP = color_text("export", ColorEnum.OKBLUE)

PROMPT = f"Enter a command ({SUB}, {REV}, or {EXP}) "
PUZZLE_PRFX = color_text("Puzzle".ljust(10), [ColorEnum.FAIL, ColorEnum.BOLD])
SOLN_PRFX = color_text("Solution".ljust(10), [ColorEnum.HEADER, ColorEnum.BOLD])

SOURCE = color_text("Source", [ColorEnum.BOLD, ColorEnum.UNDERLINE])
TARGET = color_text("Target", [ColorEnum.BOLD, ColorEnum.UNDERLINE])


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
                raise ValueError("Nothing valid to revert")

        for letter in letters:
            self.cipher[letter] = letter

    def export(self):

        print(f"{SOURCE:<7s} --> {TARGET:<7s}")
        for s, t in self.cipher.items():
            s, t = s.center(6), t.center(6)
            if s != t:
                s = color_text(s, [ColorEnum.BOLD, ColorEnum.FAIL])
                t = color_text(t, [ColorEnum.BOLD, ColorEnum.OKBLUE])

            print(f"{s} --> {t}")

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
                    soln_line.write(color_text(s, [ColorEnum.UNDERLINE, ColorEnum.OKGREEN]))

            print(f"{PUZZLE_PRFX}: {puzz}")
            print(f"{SOLN_PRFX}: {soln_line.getvalue()}")

    def run(self):

        try:
            while True:
                self.print()
                try:
                    self.process_command(input(PROMPT))
                except ValueError as e:
                    print(color_text(e, ColorEnum.FAIL))
                    continue

        except KeyboardInterrupt:
            print("Quitting")
            sys.exit(0)


if __name__ == "__main__":
    pass
