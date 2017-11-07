# Interpreter
# 
# Filename: Interpreter.py
# Description: 
# Author:    Juan Trejo
# Github:    https://github.com/jtrejo13

from typing import IO, List

# ------------
# interp_read
# ------------

def interp_read():
	pass

# ------------
# interp_eval
# ------------

def interp_eval():
	pass

# ------------
# interp_print
# ------------

def interp_print():
	pass

# ------------
# interp_print
# ------------

def interp_solve(reader: IO[str], writer: IO[str]):
	"""
	reader with input
	writer for output
	"""
	for line in reader:
		interp_read(line)
		interp_eval()
		interp_print()

