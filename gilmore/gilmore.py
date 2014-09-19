"""Gilmore's algorithm implementation."""

from syntax_tree import *
from skolemize import skolemize, eliminate_universal_quantifiers
from herbrand import HerbrandUniverse, fetch_variables
from dnf import dnf, print_dnf
from sys import stdout
from itertools import product

def go_gilmore(formula):
	prepd_formula = formula.nnf()
	prepd_formula = prepd_formula.prenex()
	prepd_formula = skolemize(prepd_formula, [])
	prepd_formula = eliminate_universal_quantifiers(prepd_formula)

	print "-- TRANSFORMED FORMULA --"
	prepd_formula.print_me()
	print

	universe = HerbrandUniverse(prepd_formula)
	variables = fetch_variables(prepd_formula)

	current_level = universe.get_current_level()
	num_vars = len(variables)

	for gilm in range(0,5):
		substitutions = list(product(current_level, repeat=num_vars))
		subd_formula = prepd_formula

		for i in range(0, num_vars):
			subd_formula = subd_formula.substitute_variable(variables[i], substitutions[0][i])

		for i in range(1, len(substitutions)):
			new_subd_formula = prepd_formula
			for j in range(0, num_vars):
				new_subd_formula = new_subd_formula.substitute_variable(variables[j], substitutions[i][j])

			subd_formula = And(subd_formula, new_subd_formula)

		print
		print "-- DNF WITH SUBSTITUTION --"
		dnf_formula = dnf(subd_formula)
		print_dnf(dnf_formula)
		print "---------"

		remove_count = 0

		for clause in dnf_formula:
			found_positive = []
			found_negative = []

			for literal in clause:
				if literal.get_type() is OperandTypes.T_NOT:
					if literal.get_formula() in found_positive:
						remove_count += 1
						break
					else:
						found_negative.append(literal.get_formula())
				elif literal.get_type() is OperandTypes.T_ATOM:
					if literal in found_negative:
						remove_count += 1
						break
					else:
						found_positive.append(literal)
				else:
					raise Exception("What the fuck exception.")


		if remove_count == len(dnf_formula):
			print "UNSAT!"
			break
		else:
			print "Removed: %d out of %d" %(remove_count, len(dnf_formula))
			print "Not working :("

		current_level = universe.next_level()
