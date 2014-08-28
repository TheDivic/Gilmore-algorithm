"""Skolemization test"""
from syntax_tree import *
from skolemize import skolemize
import pdb

def print_formula(formula):
	"""Prints a formula with a whitespace"""
	formula.print_me()
	print

s = Signature()
s.add_predicate_symbol("man",1)
s.add_predicate_symbol("woman", 1)

x_var = VariableTerm('x')
y_var = VariableTerm('y')

atom1 = Atom(s, "man", [x_var])
atom2 = Atom(s, "woman", [y_var])

print_formula(atom1)
print_formula(atom2)

imp1 = Imp(atom1, atom2)

print_formula(imp1)

exists1 = Exists(x_var, imp1)
print_formula(exists1)

print
print "-"*21 + "\n" + "--- SKOLEMIZATION ---\n" + "-"*21 +"\n"

skolemized = skolemize(exists1)
print_formula(skolemized)

print
