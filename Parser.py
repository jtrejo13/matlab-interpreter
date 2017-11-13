"""
Filename: Parser.py
Description: Tokenizer or Scanner to break input into valid MATLAB tokens
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

# -------
# imports
# -------

from Scanner import *


class Node(object):
    def __init__(self):
        self.left = None
        self.token = None
        self.right = None


class Compound(Node):
    def __init__(self):
        Node.__init__(self)
        self.statements = []


class BinaryOp(Node):
    def __init__(self, left, op, right):
        Node.__init__(self)
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(Node):
    def __init__(self, op, right):
        Node.__init__(self)
        self.right = right
        self.token = self.op = op


class Assign(Node):
    def __init__(self, left, op, right):
        Node.__init__(self)
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(Node):
    def __init__(self, token):
        Node.__init__(self)
        self.token = token


class Num(Node):
    def __init__(self, token):
        Node.__init__(self)
        self.token = token


class Parser(object):

    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = scanner.next_token()

    def parse(self):
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
        if token_type == self.current_token.type:
            self.current_token = self.scanner.next_token()
        else:
            self.raise_error()

    def raise_error(self):
        raise Exception('Invalid syntax error.')


def print_tree(tree, indent=3):
    if tree.right:
        print_tree(tree.right, indent + 4)
        print(indent * ' ' + '  /')
    print(indent * ' ' + str(tree.token))
    if tree.left:
        print(indent * ' ' + '  \\')
        print_tree(tree.left, indent + 4)


def get_expr(tree):
    l = []
    print_expr_recurs(tree, l)
    return ''.join(str(i) for i in l)


def print_expr_recurs(tree, output):
    if tree.left:
        print_expr_recurs(tree.left, output)
    if tree.right:
        output.append(tree.token.value)
        print_expr_recurs(tree.right, output)
    if not tree.left and not tree.right:
        output.append(tree.token.value)
