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
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)


class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __str__(self):
		return 'Token({type}, {value})'.format(
			type  = self.type,
			value = repr(self.value)
		)

class Scanner(object):
	def __init__(self, input) -> None:
		self.input = input