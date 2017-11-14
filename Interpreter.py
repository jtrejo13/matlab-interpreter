# pylint: disable = unused-wildcard-import
# pylint: disable = too-few-public-methods
# pylint: disable = no-self-use
# pylint: disable = invalid-name

"""
Filename: Interpreter.py
Description:
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

# -------
# imports
# -------

from typing import IO, Dict
from Scanner import *
from Parser import Parser


class NodeVisitor(object):
    """
    Generic NodeVisitor class to redirect a specific Node
    type in the Abstract Syntax Tree to its custom 'visit' method
    """

    def visit(self, node):
        """
        Generic NodeVisitor class to apply a 'visit' method based
        on the Node type observed in the Abstract Syntax Tree
        """
        method_name = 'visit_' + type(node).__name__
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node):
        """
        Falback method if node passed to visit does not have a custom visit method
        """
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    """
    Interpreter to traverse an Abstract Syntax Tree representing
    a script in the MATLAB language. As the interpreter traverses
    the tree, it evaluates expressions

    Args:
        parser(Parser): The parser constructed with the
        input to be interpreted

    Attributes:
        parser(Parser): The parser constructed with the
        input to be interpreted
        GLOBAL_SCOPE(dict key:str value:float or int) Scope of
        variables in script
    """

    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}   # variable_name : value

    def interpret(self):
        """Interprets the passed AST"""
        tree = self.parser.parse()
        if tree is None:
            return ''
        self.visit(tree)

    def visit_Compound(self, node):
        """Custom visitor method for Compound Node"""
        for statement in node.statements:
            self.visit(statement)

    def visit_Assign(self, node):
        """
        Custom visitor method for Assign Node. Defines or updates an
        identifier in GLOBAL_SCOPE when assignment node is encountered
        """
        var_name = node.left.token.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Node(self, node):
        """Custom visitor method for Node"""
        pass

    def visit_BinaryOp(self, node):
        """
        Custom visitor method for BinaryOp Node

        Returns:
            int or float: The result of a binary operation

        Raises:
            Exception: If ill-conditioned AST
        """
        token = node.token
        if token.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if token.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if token.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if token.type == DIV:
            result = self.visit(node.left) / self.visit(node.right)
            if result.is_integer():
                return int(result)
            return result
        self.raise_error()

    def visit_UnaryOp(self, node):
        """
        Custom visitor method for UnaryOp Node

        Returns:
            int or float: The result of a unary operation

        Raises:
            Exception: If ill-conditioned AST
        """
        token = node.token
        if token.type == PLUS:
            return self.visit(node.right)
        if token.type == MINUS:
            return -1 * self.visit(node.right)
        self.raise_error()

    def visit_Var(self, node):
        """
        Custom visitor method for Var Node

        Returns:
            int or float: The value of the token in the ID node

        Raises:
            NameError exception if identifier reached has
            not been declared earlier in the tree (i.e is
            not in GLOBAL_SCOPE)
        """
        var_name = node.token.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError(repr(var_name))
        else:
            return value

    def visit_Num(self, node):
        """
        Custom visitor method for Num Node

        Returns:
            int or float: The value of the token in the node
        """
        token = node.token
        if token.type in (INTEGER, FLOAT):
            return token.value

    def raise_error(self):
        """
        Raises:
            Exception: Error interpreting input
        """
        raise Exception('Error interpreting input')


# ------------
# interp_read
# ------------

def interp_read(text: str):
    """
    text to evaluate
    """
    return Parser(Scanner(text))
# ------------
# interp_eval
# ------------


def interp_eval(parser: Parser):
    """
    parser to evaluate input
    """
    interp = Interpreter(parser)
    interp.interpret()
    return interp.GLOBAL_SCOPE

# ------------
# interp_print
# ------------


def interp_print(writer: IO[str], result: Dict):
    """
    writer for output
    result to be printed
    """
    output = []
    for key in result:
        output.append(str(key) + '=' + str(result[key]))
    writer.write(str('\n'.join(output)) + '\n')

# ------------
# interp_solve
# ------------


def interp_solve(reader: IO[str], writer: IO[str]):
    """
    reader with input
    writer for output
    """
    statements = []
    for line in reader:
        statements.append(line)
    script = ''.join(statements)
    parser = interp_read(script)
    result = interp_eval(parser)
    interp_print(writer, result)
