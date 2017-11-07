# RunInterpreter
# 
# Filename: RunInterpreter.py
# Description:
# Author:    Juan Trejo
# Github:    https://github.com/jtrejo13

# -------
# imports
# -------

from sys		 import stdin, stdout

from Interpreter import interpreter_solve

# ----
# main
# ----

if __name__ == "__main__":
    interpreter_solve(stdin, stdout)