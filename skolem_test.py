"""Skolemization test"""
from syntax_tree import *
from skolemize import skolemize

s = Signature()
s.add_predicate_symbol("man",1)

x_var = VariableTerm('x')

atom1 = Atom(s, "man", [x_var])

atom1.print_me()
print

atom2 = skolemize(atom1)
atom2.print_me()
print
