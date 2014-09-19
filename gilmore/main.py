# This is where we test our program

from syntax_tree import *
from skolemize import skolemize, eliminate_universal_quantifiers
from dnf import dnf
from herbrand import fetch_constants, fetch_functions,fetch_variables, HerbrandUniverse
import pdb
from gilmore import go_gilmore

def print_formula(formula):
	"""Prints a formula with a whitespace"""
	formula.print_me()
	print

x_var = VariableTerm("x")
b_const = ConstantTerm("b")
brije1 = Atom("brije", [x_var, x_var])
brije2 = Atom("brije", [b_const, x_var])
not_brije1 = Not(brije1)
equiv = Iff(brije2, not_brije1)
forall1 = Forall(x_var, equiv)
exists1 = Exists(b_const, forall1)

go_gilmore(exists1)

