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
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF'
)


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

            if self.current_char is ' ':
                self.skip_whitespace()
                if self.current_char is None:
                    break

            if self.current_char.isdigit():
                num = self.get_integer()
                return Token(INTEGER, num)

            if self.current_char is '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char is '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char is '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char is '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char is '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char is ')':
                self.advance()
                return Token(RPAREN, ')')

            self.raise_error()

        return Token(EOF, None)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None \
                and self.current_char is ' ':
            self.advance()

    def get_integer(self):
        start = self.pos
        while self.current_char is not None \
                and self.current_char.isdigit():
            self.advance()
        return self.text[start:self.pos]

    def raise_error(self):
        raise Exception('Invalid character')
