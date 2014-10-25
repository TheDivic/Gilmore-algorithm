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

# # ~(Eb.Ax. brije(b,x) <==> ~brije(x,x))
# x_var = VariableTerm("x")
# b_const = ConstantTerm("b")
# brije1 = Atom("brije", [x_var, x_var])
# brije2 = Atom("brije", [b_const, x_var])
# not_brije1 = Not(brije1)
# equiv = Iff(brije2, not_brije1)
# forall1 = Forall(x_var, equiv)
# exists1 = Exists(b_const, forall1)

# print_formula(exists1)
# go_gilmore(exists1)

# q = raw_input("Next formula?")
# # Ax. P(x) => Ay. P(y)
# x_var = VariableTerm("x")
# y_var = VariableTerm("y")
# p_atom1 = Atom("P", [x_var])
# p_atom2 = Atom("P", [y_var])
# forall_y = Forall(y_var, p_atom2)
# forall_x = Forall(x_var, p_atom1)
# imply = Imp(forall_x, forall_y)
# prove_valid(imply)
# ((Ax.Ey.p(x,y)) /\ (Ax.Ay.p(x,y) => q(x,y))) => Ax.Ey.p(x,y)
x_var = VariableTerm("x")
y_var = VariableTerm("y")
p_atom = Atom("p", [x_var, y_var])
q_atom = Atom("q", [x_var, y_var])
exists1 = Exists(y_var, p_atom)
forall2 = Forall(x_var, exists1)
imp1 = Imp(p_atom, q_atom)
forall3 = Forall(y_var, imp1)
forall4 = Forall(x_var, forall3)
and1 = And(forall2, forall4)
exists2 = Exists(y_var, q_atom)
forall5 = Forall(x_var, exists2)
imp2 = Imp(and1, forall5)
imp2 = Not(imp2)
print "Starting formula:"
imp2.print_me()
print
prove_valid(imp2)

