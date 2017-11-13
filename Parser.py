"""
Filename: Parser.py
Description: Parser of the MATLAB language
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

# -------
# imports
# -------

from Scanner import *


class Node(object):
    """Base class representing a binary tree node"""

    def __init__(self):
        self.left = None
        self.token = None
        self.right = None


class Compound(Node):
    """
    Node sub-class to represent a Compound element in a MATLAB 
    Abstract Syntax Tree. In this implementation the Compound
    element is the whole script

    Attributes:
        statements(list of Node): The statements included in the MATLAB script
    """

    def __init__(self):
        Node.__init__(self)
        self.statements = []


class BinaryOp(Node):
    """
    Node sub-class to represent a 'binary operation' in
    a MATLAB Abstract Syntax Tree. Examples: 2 * 3 or 10 / 2

    Attributes:
    left(Node): The child Node on the left
    right(Node): The child Node on the right
    token(Token): A binary operator token.
    """

    def __init__(self, left, op, right):
        Node.__init__(self)
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(Node):
    """
    Node sub-class to represent a 'unary operation' in 
    a MATLAB Abstract Syntax Tree. Examples: --1 or -(+2)

    Attributes:
    right(Node): The child Node on the right
    token(Token): A unary operator token
    """

    def __init__(self, op, right):
        Node.__init__(self)
        self.right = right
        self.token = op


class Assign(Node):
    """
    Node sub-class to represent an 'assignment' in 
    a MATLAB Abstract Syntax Tree. Examples: x = 2, myVar = 2 * 3 + 5

    Attributes:
    left(Var): The child Var on the left
    right(Node): The child Node on the right
    token(Token): An assignment token
    """

    def __init__(self, left, op, right):
        Node.__init__(self)
        self.left = left
        self.token = op
        self.right = right


class Var(Node):
    """
    Node sub-class to represent a 'variable' or 'identifier' 
    in a MATLAB Abstract Syntax Tree. Examples: myVar, PI, area

    Attributes:
    token(Token): An ID token
    """

    def __init__(self, token):
        Node.__init__(self)
        self.token = token


class Num(Node):
    """
    Node sub-class to represent a positive numer in
    a MATLAB Abstract Syntax Tree. Examples: 3.14159, 10

    Attributes:
    token(Token): A FLOAT or INTEGER token
    """

    def __init__(self, token):
        Node.__init__(self)
        self.token = token


class Parser(object):
    """
    A class to parse a series of tokens representing the MATLAB language

    Args:
        scanner(Scanner): A scanner object constructed with the text input to be parsed

    Attributes:
        scanner(Scanner): A scanner object constructed with the text input to be parsed
        current_token(Token): The current token being analyzed by the parser
    """

    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = scanner.next_token()

    def parse(self):
        """
        Parses the text input passed via the scanner

        Returns:
            Node: An Abstract Syntax Tree (AST) representing the input passed

        Raises:
            Exception: If invalid syntax is encountered
        """
        node = self.script()
        if self.current_token.type != EOF:
            self.raise_error()

        return node

    def script(self):
        nodes = self.statement_list()

        root = Compound()
        for node in nodes:
            root.statements.append(node)

        return root

    def statement_list(self):
        node = self.statement()

        statements = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            statements.append(self.statement())

        if self.current_token.type == ID:
            self.raise_error()

        return statements

    def statement(self):
        if self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = Node()  # empty node
        return node

    def assignment_statement(self):
        variable = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        expr = self.expr()
        node = Assign(variable, token, expr)
        return node

    def expr(self):
        node = self.term()

        while self.current_token.type == PLUS or \
                self.current_token.type == MINUS:
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinaryOp(node, token, self.term())
        return node

    def term(self):
        node = self.factor()

        while self.current_token.type == MUL or \
                self.current_token.type == DIV:
            token = self.current_token
            if self.current_token.type == MUL:
                self.eat(MUL)
            elif self.current_token.type == DIV:
                self.eat(DIV)
            node = BinaryOp(node, token, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node
        self.raise_error()

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def eat(self, token_type):
        """Advances parser by a single token"""
        if token_type == self.current_token.type:
            self.current_token = self.scanner.next_token()
        else:
            self.raise_error()

    def raise_error(self):
        """
        Raises:
            Exception: Invalid sytax error
        """
        raise Exception('Invalid syntax error.')


"""
def print_tree(tree, indent=3):
    if tree.right:
        print_tree(tree.right, indent + 4)
        print(indent * ' ' + '  /')
    print(indent * ' ' + str(tree.token))
    if tree.left:
        print(indent * ' ' + '  \\')
        print_tree(tree.left, indent + 4)
"""


def get_expr(tree):
    """
    Converts an AST back into the original 'linear' expression.

    Args:
        tree(Node): The root of an AST to be 'linearized'

    Returns:
        str: String representation of expression

    Examples:
        parser = Parser(Scanner('x = 2 + 5'))
        myAST = parser.parse()
        expression = get_expr(myAST)
        expression == 'x=2+5'
    """
    elems = []
    print_expr_recurs(tree, elems)
    return ''.join(str(item) for item in elems)


def print_expr_recurs(tree, output):
    """Helper recursive function for print_expr"""
    if tree.left:
        print_expr_recurs(tree.left, output)
    if tree.right:
        output.append(tree.token.value)
        print_expr_recurs(tree.right, output)
    if not tree.left and not tree.right:
        output.append(tree.token.value)
