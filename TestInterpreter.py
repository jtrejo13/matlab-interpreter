# pylint: disable = missing-docstring

"""
Filename: TestInterpreter.py
Description:
Author:    Juan Trejo
Github:    https://github.com/jtrejo13
"""

# -------
# imports
# -------

from unittest import main, TestCase
from Scanner import Token, Scanner, INTEGER, PLUS
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
        result_tokens = []
        for _ in range(0, 9):
            result_tokens.append(scanner.next_token())

        expected = ('[Token(MINUS, -), Token(INTEGER, 5), Token(MUL, *),'
        ' Token(LPAREN, (), Token(INTEGER, 3), Token(DIV, /),'
        ' Token(INTEGER, 2), Token(RPAREN, )), Token(EOF, None)]')
        self.assertEqual(expected, str(result_tokens))

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

    def test_scanner_next_token_7(self):
        scanner = Scanner('myVar = 2;')
        result_tokens = []
        for _ in range(0, 5):
            result_tokens.append(scanner.next_token())

        expected = ('[Token(ID, myVar), Token(ASSIGN, =), Token(INTEGER, 2),' ' Token(SEMI, ;), Token(EOF, None)]')
        self.assertEqual(expected, str(result_tokens))

# ----------
# TestParser
# ----------

class TestParser(TestCase):

    def test_parser_parse_0(self):
        scanner = Scanner('x = 2')
        parser = Parser(scanner)
        tree = parser.parse()
        statement = tree.statements[0]
        self.assertEqual(get_expr(statement), 'x=2')

    def test_parser_parse_1(self):
        scanner = Scanner('myVar = 2 + 2')
        parser = Parser(scanner)
        tree = parser.parse()
        statement = tree.statements[0]
        self.assertEqual(get_expr(statement), 'myVar=2+2')

    def test_parser_parse_2(self):
        scanner = Scanner('var1 = 1+2+3;')
        parser = Parser(scanner)
        tree = parser.parse()
        statement = tree.statements[0]
        self.assertEqual(get_expr(statement), 'var1=1+2+3')

    def test_parser_parse_3(self):
        scanner = Scanner('res = 1 + (2 * 3) - 45 + 2 * (14  / 7);')
        parser = Parser(scanner)
        tree = parser.parse()
        statement = tree.statements[0]
        self.assertEqual(get_expr(statement), 'res=1+2*3-45+2*14/7')

    def test_parser_parse_4(self):
        scanner = Scanner('invalid = 3~2')
        parser = Parser(scanner)
        with self.assertRaises(Exception) as _:
            tree = parser.parse()

    def test_parser_parse_5(self):
        scanner = Scanner('myInt = -+-1')
        parser = Parser(scanner)
        tree = parser.parse()
        statement = tree.statements[0]
        self.assertEqual(get_expr(statement), 'myInt=-+-1')

    def test_parser_parse_6(self):
        scanner = Scanner('var = 3++')
        parser = Parser(scanner)
        with self.assertRaises(Exception) as _:
            tree = parser.parse()

    def test_parser_parse_7(self):
        scanner = Scanner('x = 3+2')
        parser = Parser(scanner)
        with self.assertRaises(Exception) as _:
            parser.eat(DIV)

    def test_parser_parse_8(self):
        scanner = Scanner('var')
        parser = Parser(scanner)
        with self.assertRaises(Exception) as _:
            tree = parser.parse()

    def test_parser_parse_9(self):
        scanner = Scanner('x = 3;\n y = 2;')
        parser = Parser(scanner)
        tree = parser.parse()
        statements = tree.statements
        self.assertEqual(get_expr(statements[0]), 'x=3')
        self.assertEqual(get_expr(statements[1]), 'y=2')

    def test_parser_parse_10(self):
        script = (' x1 = 1 + (2*3) - 45 + ( 2 * 14/7);  \n'
        'y = ((2)*5)/5 + 15;')
        scanner = Scanner(script)
        parser = Parser(scanner)
        tree = parser.parse()
        statements = tree.statements
        self.assertEqual(get_expr(statements[0]), 'x1=1+2*3-45+2*14/7')
        self.assertEqual(get_expr(statements[1]), 'y=2*5/5+15')

    def test_parser_parse_9(self):
        scanner = Scanner('x = 3;\n y = x;')
        parser = Parser(scanner)
        tree = parser.parse()
        statements = tree.statements
        self.assertEqual(get_expr(statements[0]), 'x=3')
        self.assertEqual(get_expr(statements[1]), 'y=x')


# ---------------
# TestInterpreter
# ---------------


class TestInterpreter(TestCase):

    def test_interp_express_0(self):
        scanner = Scanner('x = 1;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        self.assertEqual('{\'x\': 1}', str(interp.GLOBAL_SCOPE))

    def test_interp_express_1(self):
        scanner = Scanner('res = 14 + 2 * 3 - 6 / 2 + 10;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        self.assertEqual('{\'res\': 27.0}', str(interp.GLOBAL_SCOPE))

    def test_interp_express_2(self):
        scanner = Scanner('res = 8 + 3 * (10 / (12 / (3 + 1) - 1)) * ( 10 * 5) - 5;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        self.assertEqual('{\'res\': 753.0}', str(interp.GLOBAL_SCOPE))

    def test_interp_express_3(self):
        script = """a = +-1;
                    x = 5;
                    y = x + 3;
                    res = y + 3 * ((y + 2)/(12 / (3 + 1) - 1)) * ((y+2) * x) - x;"""
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        result = {'a': -1, 'x': 5, 'y': 8, 'res': 753.0}
        self.assertEqual(result, interp.GLOBAL_SCOPE)


    def test_interp_express_4(self):
        script = '  % this is a variable \n  '
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        result = {}
        self.assertEqual(result, interp.GLOBAL_SCOPE)


    def test_interp_express_5(self):
        script = 'x = 5;  % this is a variable \n  '
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        result = {'x': 5}
        self.assertEqual(result, interp.GLOBAL_SCOPE)


    def test_interp_express_6(self):
        script = """a = +-1;
                    x = 5;          % this is x
                    y = x + 3;      % this is y
                    
                    % The result 
                    res = y + 3 * ((y + 2)/(12 / (3 + 1) - 1)) * ((y+2) * x) - x;"""
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        result = {'a': -1, 'x': 5, 'y': 8, 'res': 753.0}
        self.assertEqual(result, interp.GLOBAL_SCOPE)


#     def test_interp_express_3(self):
#         scanner = Scanner('14 + 2 * 3 - 6 / 2 + 10')
#         parser = Parser(scanner)
#         interp = Interpreter(parser)
#         self.assertEqual(interp.interpret(), 27)

#     def test_interp_express_4(self):
#         scanner = Scanner(
#             '8 + 3 * (10 / (12 / (3 + 1) - 1)) * ( 10 * 5) - 5')
#         parser = Parser(scanner)
#         interp = Interpreter(parser)
#         self.assertEqual(interp.interpret(), 753)

#     def test_interp_express_5(self):
#         scanner = Scanner('7 + (((3 + 2)))')
#         parser = Parser(scanner)
#         interp = Interpreter(parser)
#         self.assertEqual(interp.interpret(), 12)

#     def test_interp_express_6(self):
#         bad_tree = BinaryOp(Token(MUL, '*'), Token(MUL, '*'), 3)
#         interp = Interpreter(bad_tree)
#         with self.assertRaises(Exception) as _:
#             interp.vist(bad_tree)

# ----
# main
# ----


if __name__ == '__main__':  # pragma: no cover
    main()
