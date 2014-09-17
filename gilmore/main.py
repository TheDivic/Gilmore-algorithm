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
forall_brije2 = Forall(x_var, brije2)
exists_forall_brije2 = Exists(b_const, forall_brije2)
eqiv = Iff(exists_forall_brije2, not_brije1)
not_equiv = Not(eqiv)

go_gilmore(not_equiv)

