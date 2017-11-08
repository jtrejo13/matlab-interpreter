"""
Filename: Interpreter.py
Description:
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

from typing import IO
from Scanner import Scanner
from Parser import Parser

# ------------
# interp_read
# ------------


def interp_read(input: str):
    return Parser(Scanner(input))


# ------------
# interp_eval
# ------------

def interp_eval(scanner):
    return "1"

# ------------
# interp_print
# ------------


def interp_print(writer: IO[str], result: str):
    writer.write(result + "\n")


# ------------
# interp_solve
# ------------

def interp_solve(reader: IO[str], writer: IO[str]):
    """
    reader with input
    writer for output
    """
    for line in reader:
        parser = interp_read(line)
        result = interp_eval(parser)
        interp_print(writer, result)
