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
        self.GLOBAL_SCOPE = {}   # variable_name : value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_Compound(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Assign(self, node):
        var_name = node.left.token.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Node(self, node):
        pass

    def visit_BinaryOp(self, node):
        token = node.token
        if token.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if token.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if token.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if token.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        self.raise_error()

    def visit_UnaryOp(self, node):
        token = node.token
        if token.type == PLUS:
            return self.visit(node.right)
        if token.type == MINUS:
            return -1 * self.visit(node.right)
        self.raise_error()

    def visit_Var(self, node):
        var_name = node.token.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError(repr(token.value))
        else:
            return value
            
    def visit_Num(self, node):
        token = node.token
        if token.type == INTEGER:
            return token.value

    def raise_error(self):
        raise Exception('Error parsing input')


# ------------
# interp_read
# ------------

def interp_read(line: str):
    return Parser(Scanner(line))

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
    writer.write(str(result) + '\n')

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
