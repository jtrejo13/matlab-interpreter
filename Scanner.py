"""
Filename: Scanner.py
Description: Tokenizer or Scanner to break input into valid MATLAB tokens
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

"""
Token types

EOF (end-of-file) token is used to indicate that
there is no more input left for lexical analysis
"""
ID, INTEGER, ASSIGN, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, SEMI, EOF = (
    'ID', 'INTEGER', 'ASSIGN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'SEMI', 'EOF'
)

RESERVED_KEYWORDS = {}


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()


class Scanner(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        try:
            self.current_char = self.text[self.pos]
        except:
            self.current_char = None

    def next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                if self.current_char is None:
                    break

            if self.current_char.isdigit():
                num = self.get_integer()
                return Token(INTEGER, num)

             if self.current_char == '%':

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char.isalnum():
                return self._id()

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            self.raise_error()

        return Token(EOF, None)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None \
                and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        start = self.pos
        while self.current_char is not None \
                and self.current_char.isdigit():
            self.advance()
        return int(self.text[start:self.pos])

    def _id(self):
        start = self.pos
        while self.current_char is not None \
                and self.current_char.isalnum():
            self.advance()

        result = self.text[start:self.pos]
        return RESERVED_KEYWORDS.get(result, Token(ID, result))

    def raise_error(self):
        raise Exception('Invalid character')
