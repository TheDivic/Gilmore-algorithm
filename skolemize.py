"""A module that contains the Skolemize function that eliminates the existential quantifiers from the formula."""
import copy
from syntax_tree import *

def skolemize(formula):
	formula_switch = { OperandTypes.T_ATOM : skolemize_atom }
	return formula_switch[formula.get_type()](formula)

def skolemize_atom(formula):
	print("Skolemizing!")
	return copy.deepcopy(formula)