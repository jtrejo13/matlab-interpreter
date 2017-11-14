# pylint: disable = unused-wildcard-import
# pylint: disable = too-few-public-methods

"""
Filename: Scanner.py
Description: Tokenizer to break text input into tokens
             The tokenizer is built to suport a MATLAB script with basic
             functionality as input
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

# -------
# imports
# -------

from typing import Dict

# ----------------------------------------------------
# Token Types
#
# ID (variable name): used to represent an identifier,
# or variable, in the program
#
# EOF (end-of-file): token is used to indicate that
# there is no more input left for lexical analysis
# ----------------------------------------------------
ID, INTEGER, FLOAT, ASSIGN, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, SEMI, EOF = (
    'ID', 'INTEGER', 'FLOAT', 'ASSIGN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'SEMI', 'EOF'
)


"""
Reserved Keywords

Words that cannot be used as identifier, such as the name
of a variable or function
"""
RESERVED_KEYWORDS = {}  # type: Dict[str, Token]


class Token(object):
    """
    A class to represent a valid token in a MATLAB script

    Args:
        type  (Token Type): The type of the token
        value (str_int_or_float): The value of the token

    Attributes:
        type  (Token Type): The type of the token
        value (str_int_or_float): The value of the token
    """

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        Returns:
            str: String representation of token

        Examples:
            'Token(INTEGER, 2)'
            'Token(FLOAT, 3.5)'
            'Token(MINUS, -)'
            'Token(ID, myVar)'
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        """String representation of token"""
        return self.__str__()


class Scanner(object):
    """
    Tokenizer of a MATLAB script

    Args:
        text(str): The input text to be tokenized

    Attributes:
        text(str): The input text to be tokenized
    """

    def __init__(self, text):
        self.text = text
        self._pos = 0
        try:
            self.current_char = self.text[self._pos]
        except IndexError:
            self.current_char = None

    def next_token(self):
        """
        Scans and outputs the next token in the input text
        Returns:
            token(Token): The next valid token in the input text.
            If EOF file is reached, returns (EOF, None) token
        Raises:
            Expection: If invalid charcter is provided
        """
        while self.current_char is not None:

            if self.current_char == '%':
                self._skip_comment()
                continue

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = self.get_number()
                return token

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

            self.raise_error()  # if invalid character

        return Token(EOF, None)

    def get_number(self):
        """Scans input for a real or integer number"""
        start = self._pos
        while self.current_char is not None \
                and (self.current_char.isdigit() or self.current_char == '.'):
            self.advance()
        result = self.text[start:self._pos]
        period_count = result.count('.')
        if period_count > 1:
            self.raise_error()
        elif period_count == 1:
            return Token(FLOAT, float(result))
        else:
            return Token(INTEGER, int(result))

    def _id(self):
        start = self._pos
        while self.current_char is not None \
                and self.current_char.isalnum():
            self.advance()

        result = self.text[start:self._pos]
        return RESERVED_KEYWORDS.get(result, Token(ID, result))

    def advance(self):
        """Advances internal pointer by one character"""
        self._pos += 1
        if self._pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self._pos]

    def peek(self):
        """
        Looks at one character past the current position
        Returns:
            character(str): The character next to the current position
        """
        peek_pos = self._pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        # else: still in bounds
        return self.text[peek_pos]

    def _skip_comment(self):
        while self.current_char is not None \
                and self.current_char != '\n':
            self.advance()

    def skip_whitespace(self):
        """
        Skips all whitespace in input up to the next
        non-whitespace character or until the EOF is reached
        """
        while self.current_char is not None \
                and self.current_char.isspace():
            self.advance()

    def raise_error(self):
        """
        Raises:
            Exception: Invalid character exception
        """
        raise Exception('Invalid character')
