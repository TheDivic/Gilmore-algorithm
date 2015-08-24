# This is where we test our program

from syntax_tree import *
from skolemize import skolemize, eliminate_universal_quantifiers
from dnf import dnf
from herbrand import fetch_constants, fetch_functions, fetch_variables, HerbrandUniverse
import pdb
from gilmore import go_gilmore, prove_valid
from skolemize import skolemize


def print_formula(formula):
    """Prints a formula with a whitespace"""
    formula.print_me()
    print

# ~(Eb.Ax. brije(b,x) <==> ~brije(x,x))
x_var = VariableTerm("x")
b_const = ConstantTerm("b")
brije1 = Atom("brije", [x_var, x_var])
brije2 = Atom("brije", [b_const, x_var])
not_brije1 = Not(brije1)
equiv = Iff(brije2, not_brije1)
forall1 = Forall(x_var, equiv)
exists1 = Exists(b_const, forall1)
not_exists = Not(exists1)

print_formula(not_exists)
prove_valid(not_exists)


x_var = VariableTerm("x")
y_var = VariableTerm("y")

p_atom = Atom("P", [x_var, y_var])

exists_y = Exists(y_var, p_atom)
forall_x = Forall(x_var, p_atom)
x_y = Forall(x_var, exists_y)
y_x = Exists(y_var, forall_x)

imp = Imp(x_y, y_x)
imp.print_me()
print 
prove_valid(imp)



