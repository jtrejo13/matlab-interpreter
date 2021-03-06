# pylint: disable = missing-docstring
# pylint: disable = unused-wildcard-import
# pylint: disable = wildcard-import

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
from io import StringIO
from Scanner import Token, Scanner, INTEGER, PLUS
from Parser import *
from Interpreter import *

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
        with self.assertRaises(Exception):
            scanner.next_token()

    def test_scanner_next_token_7(self):
        scanner = Scanner('myVar = 2;')
        result_tokens = []
        for _ in range(0, 5):
            result_tokens.append(scanner.next_token())

        expected = """[Token(ID, myVar), Token(ASSIGN, =), Token(INTEGER, 2), Token(SEMI, ;), Token(EOF, None)]"""
        self.assertEqual(expected, str(result_tokens))

    def test_scanner_next_token_9(self):
        scanner = Scanner('2.5')
        self.assertEqual('Token(FLOAT, 2.5)', str(scanner.next_token()))

    def test_scanner_next_token_10(self):
        scanner = Scanner('2.5.0')
        with self.assertRaises(Exception):
            scanner.next_token()

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
        with self.assertRaises(Exception):
            parser.parse()

    def test_parser_parse_5(self):
        scanner = Scanner('myInt = -+-1')
        parser = Parser(scanner)
        tree = parser.parse()
        statement = tree.statements[0]
        self.assertEqual(get_expr(statement), 'myInt=-+-1')

    def test_parser_parse_6(self):
        scanner = Scanner('var = 3++')
        parser = Parser(scanner)
        with self.assertRaises(Exception):
            parser.parse()

    def test_parser_parse_7(self):
        scanner = Scanner('x = 3+2')
        parser = Parser(scanner)
        with self.assertRaises(Exception):
            parser.eat(DIV)

    def test_parser_parse_8(self):
        scanner = Scanner('var')
        parser = Parser(scanner)
        with self.assertRaises(Exception):
            parser.parse()

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

    def test_parser_parse_11(self):
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

    # -----------
    # Interpreter
    # -----------

    def test_interp_express_0(self):
        scanner = Scanner('x = 1;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.interpret()
        result = {'x': 1}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_1(self):
        scanner = Scanner('res = 14 + 2 * 3 - 6 / 2 + 10;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {'res': 27}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_2(self):
        scanner = Scanner(
            'res = 8 + 3 * (10 / (12 / (3 + 1) - 1)) * ( 10 * 5) - 5;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {'res': 753}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_3(self):
        script = """a = +-1;
                    x = 5;
                    y = x + 3;
                    res = y + 3 * ((y + 2)/(12 / (3 + 1) - 1)) * ((y+2) * x) - x;"""
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {'a': -1, 'x': 5, 'y': 8, 'res': 753}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_4(self):
        script = '  % this is a variable \n  '
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_5(self):
        script = 'x = 5;  % this is a variable \n  '
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
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
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {'a': -1, 'x': 5, 'y': 8, 'res': 753}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_7(self):
        scanner = Scanner('x = 1.53;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {'x': 1.53}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_8(self):
        scanner = Scanner('res = 14.75 + 2 * 3 - 6 / 2.5 + 10.5;')
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {'res': 28.85}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    def test_interp_express_9(self):
        script = """\
        radius = 2.5;                     % the radius
        PI = 3.14159;                     % PI constant
        area = PI * radius * radius;      % the area
        """
        scanner = Scanner(script)
        parser = Parser(scanner)
        interp = Interpreter(parser)
        interp.GLOBAL_SCOPE = {}
        interp.interpret()
        result = {'radius': 2.5, 'PI': 3.14159, 'area': 19.6349375}
        self.assertEqual(result, interp.GLOBAL_SCOPE)

    # ----
    # REPL
    # ----

    def test_interpret_read(self):
        script = """\
        x = 3;
        y = 10;
        res = x + y;
        """
        parser = interp_read(script)
        self.assertTrue(isinstance(parser, Parser))

    def test_interpret_eval(self):
        script = """\
        x = 3;
        y = 10;
        res = x + y;
        """
        expected = {'x': 3, 'y': 10, 'res': 13}
        self.assertEqual(expected, interp_eval(Parser(Scanner(script))))

    def test_interpret_print(self):
        script = """\
        x = 3;
        y = 10;
        res = x + y;
        """
        writer = StringIO()
        interp = Interpreter(Parser(Scanner(script)))
        interp.interpret()
        expected = 'x=3\ny=10\nres=13\n'
        interp_print(writer, interp.GLOBAL_SCOPE)
        self.assertEqual(len(expected), len(writer.getvalue()))

    def test_interpret_solve(self):
        reader = StringIO("x=3;\ny=10;\nres=x + y;\n")
        writer = StringIO()
        interp_solve(reader, writer)
        expected = 'x=3\ny=10\nres=13\n'
        self.assertEqual(len(expected), len(writer.getvalue()))

# ----
# main
# ----


if __name__ == '__main__':  # pragma: no cover
    main()
