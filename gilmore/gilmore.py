"""Gilmore's algorithm implementation."""

from syntax_tree import *
from skolemize import skolemize, eliminate_universal_quantifiers
from dnf import dnf

def go_gilmore(formula):
	prepd_formula = formula.nnf()
	prepd_formula = prepd_formula.prenex()
	prepd_formula = skolemize(prepd_formula, [])
	prepd_formula = eliminate_universal_quantifiers(prepd_formula)

	print "-- TRANSFORMED FORMULA --"
	prepd_formula.print_me()
	print