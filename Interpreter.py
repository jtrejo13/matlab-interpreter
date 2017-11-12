# pylint: disable = bad-whitespace
# pylint: disable = missing-docstring

"""
Filename: Interpreter.py
Description:
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

# -------
# imports
# -------

from typing import IO
from Scanner import *
from Parser import Parser


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_BinaryOp(self, node):
        token = node.token
        if token.type is PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if token.type is MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if token.type is MUL:
            return self.visit(node.left) * self.visit(node.right)
        if token.type is DIV:
            return self.visit(node.left) / self.visit(node.right)
        self.raise_error()

    def visit_UnaryOp(self, node):
        token = node.token
        if token.type is PLUS:
            return self.visit(node.right)
        if token.type is MINUS:
            return -1 * self.visit(node.right)
        self.raise_error()

    def visit_Num(self, node):
        token = node.token
        if token.type is INTEGER:
            return int(token.value)

    def raise_error(self):
        raise Exception('Error parsing input')


# ------------
# interp_read
# ------------

def interp_read(line: str):
    return Parser(Scanner(line.rstrip()))

# ------------
# interp_eval
# ------------


def interp_eval(parser: Parser):
    interp = Interpreter(parser)
    result = interp.interpret()
    return result

# ------------
# interp_print
# ------------


def interp_print(writer: IO[str], result: str):
    writer.write(str(result) + "\n")

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
