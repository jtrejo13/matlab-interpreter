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
from Scanner import *


# -----------
# TestScanner
# -----------

class TestScanner(TestCase):
    def test_token_construct(self):
        token = Token(INTEGER, 4)
        self.assertEqual("Token(INTEGER, 4)", token.__str__())


# -----------
# TestInterpreter
# -----------

class TestInterpreter(TestCase):
    def test_1(self):
        self.assertEqual(True, True)


# ----
# main
# ----

if __name__ == "__main__":  # pragma: no cover
    main()
