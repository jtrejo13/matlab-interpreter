"""
Filename: Parser.py
Description: Tokenizer or Scanner to break input into valid MATLAB tokens
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""


class Parser(object):

	def __init__(self, scanner):
		self.scanner = scanner