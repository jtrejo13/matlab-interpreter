'''
Filename: TestInterpreter.py
Description:
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
'''

# -------
# imports
# -------

from unittest import main, TestCase
from Scanner import Token, Scanner, INTEGER, PLUS, EOF
from Parser import *
from Interpreter import Interpreter

# -----------
# TestScanner
# -----------


class TestScanner(TestCase):

        # ----
        # Token
        # ----

    def test_token_construct_0(self):
        token = Token(INTEGER, 4)
        self.assertEqual('Token(INTEGER, 4)', str(token))

    def test_token_construct_1(self):
        token = Token(PLUS, '+')
        self.assertEqual('Token(PLUS, +)', str(token))

    def test_token_construct_2(self):
        token = Token(EOF, 'eof')
        self.assertEqual('Token(EOF, eof)', str(token))

    def test_token_construct_3(self):
        token1 = Token(INTEGER, 1)
        token2 = Token(INTEGER, 2)
        tokens = [token1, token2]
        self.assertEqual('[Token(INTEGER, 1), Token(INTEGER, 2)]', str(tokens))

        # -------
        # Scanner
        # -------

    def test_scanner_next_token_0(self):
        scanner = Scanner('2')
        self.assertEqual('Token(INTEGER, 2)', str(scanner.next_token()))

    def test_scanner_next_token_1(self):
        scanner = Scanner('23424')
        self.assertEqual('Token(INTEGER, 23424)',
                         str(scanner.next_token()))

    def test_scanner_next_token_2(self):
        scanner = Scanner('    424+')
        self.assertEqual('Token(INTEGER, 424)', str(scanner.next_token()))
        self.assertEqual('Token(PLUS, +)', str(scanner.next_token()))

    def test_scanner_next_token_3(self):
        scanner = Scanner('-5*(3/2)')
        self.assertEqual('Token(MINUS, -)', str(scanner.next_token()))
        self.assertEqual('Token(INTEGER, 5)', str(scanner.next_token()))
        self.assertEqual('Token(MUL, *)', str(scanner.next_token()))
        self.assertEqual('Token(LPAREN, ()', str(scanner.next_token()))
        self.assertEqual('Token(INTEGER, 3)', str(scanner.next_token()))
        self.assertEqual('Token(DIV, /)', str(scanner.next_token()))
        self.assertEqual('Token(INTEGER, 2)', str(scanner.next_token()))
        self.assertEqual('Token(RPAREN, ))', str(scanner.next_token()))

    def test_scanner_next_token_4(self):
        scanner = Scanner('1 ')
        scanner.next_token()
        self.assertEqual('Token(EOF, None)', str(scanner.next_token()))

    def test_scanner_next_token_5(self):
        scanner = Scanner('')
        scanner.next_token()
        self.assertEqual('Token(EOF, None)', str(scanner.next_token()))

    def test_scanner_next_token_6(self):
        scanner = Scanner('~')
        with self.assertRaises(Exception) as _:
            scanner.next_token()

# ----------
# TestParser
# ----------


class TestParser(TestCase):

    def test_parser_parse_0(self):
        scanner = Scanner('2')
        parser = Parser(scanner)
        tree = parser.parse()
        self.assertEqual(get_expr(tree), '2')

    def test_parser_parse_1(self):
        scanner = Scanner('2 + 2')
        parser = Parser(scanner)
        tree = parser.parse()
        self.assertEqual(get_expr(tree), '2+2')

    def test_parser_parse_2(self):
        scanner = Scanner('1+2+3')
        parser = Parser(scanner)
        tree = parser.parse()
        self.assertEqual(get_expr(tree), '1+2+3')

    def test_parser_parse_3(self):
        scanner = Scanner('1 + (2 * 3) - 45 + 2 * (14  / 2)')
        parser = Parser(scanner)
        tree = parser.parse()
        self.assertEqual(get_expr(tree), '1+2*3-45+2*14/2')

    def test_parser_parse_4(self):
        scanner = Scanner('3%2')
        parser = Parser(scanner)
        with self.assertRaises(Exception) as _:
            tree = parser.parse()

    def test_parser_parse_5(self):
        scanner = Scanner('-+-1')
        parser = Parser(scanner)
        tree = parser.parse()
        self.assertEqual(get_expr(tree), '-+-1')

    def test_parser_parse_6(self):
        scanner = Scanner('3++')
        parser = Parser(scanner)
        with self.assertRaises(Exception) as _:
            tree = parser.parse()

    def test_parser_parse_7(self):
        scanner = Scanner('3+2')
        parser = Parser(scanner)
        with self.assertRaises(Exception) as _:
            parser.eat(DIV)

# ---------------
# TestInterpreter
# ---------------


class TestInterpreter(TestCase):

    def test_interp_express_0(self):
        scanner = Scanner('1')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        self.assertEqual(interp.interpret(), 1)

    def test_interp_express_1(self):
        scanner = Scanner('-+--1')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        self.assertEqual(interp.interpret(), -1)

    def test_interp_express_2(self):
        scanner = Scanner('1 + 1')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        self.assertEqual(interp.interpret(), 2)

    def test_interp_express_3(self):
        scanner = Scanner('14 + 2 * 3 - 6 / 2')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        self.assertEqual(interp.interpret(), 17)

    def test_interp_express_4(self):
        scanner = Scanner(
            '7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        self.assertEqual(interp.interpret(), 10)

    def test_interp_express_5(self):
        scanner = Scanner('7 + (((3 + 2)))')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        self.assertEqual(interp.interpret(), 12)

    def test_interp_express_6(self):
        bad_tree = BinaryOp(Token(MUL, '*'), Token(MUL, '*'), 3)
        interp = Interpreter(bad_tree)
        with self.assertRaises(Exception) as _:
            interp.vist(bad_tree)

# ----
# main
# ----


if __name__ == '__main__':  # pragma: no cover
    main()
