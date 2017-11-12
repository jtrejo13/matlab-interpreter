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


class Num(Node):
    def __init__(self, token):
        Node.__init__(self)
        self.token = token
        self.value = token.value


class Parser(object):

    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = scanner.next_token()

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()

        while self.current_token.type is PLUS or \
                self.current_token.type is MINUS:
            token = self.current_token
            if token.type is PLUS:
                self.eat(PLUS)
            elif token.type is MINUS:
                self.eat(MINUS)
            node = BinaryOp(node, token, self.term())
        return node

    def term(self):
        node = self.factor()

        while self.current_token.type is MUL or \
                self.current_token.type is DIV:
            token = self.current_token
            if self.current_token.type is MUL:
                self.eat(MUL)
            elif self.current_token.type is DIV:
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
        else:
            if token.type == INTEGER:
                self.eat(INTEGER)
                return Num(token)
            elif token.type == LPAREN:
                self.eat(LPAREN)
                node = self.expr()
                self.eat(RPAREN)
                return node
        self.raise_error()

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
