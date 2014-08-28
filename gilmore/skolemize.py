"""A module that contains the Skolemize function.

Skolemization eliminates the existential quantifiers from the formula."""
import copy
from syntax_tree import OperandTypes, get_unique_constant, ConstantTerm

def skolemize(formula, quantified_varible_list=[]):
    """Skolemizes (eliminates the existential quantifiers) the given formula.

        We assume that the formula is in the prenex  form.
    """
    formula_type = formula.get_type()

    not_quantifiers = [OperandTypes.T_ATOM, OperandTypes.T_NOT,\
    OperandTypes.T_AND, OperandTypes.T_OR, OperandTypes.T_IMP, \
    OperandTypes.T_IFF]

    if formula_type in not_quantifiers:
        return skolemize_non_quantifier(formula)

    elif formula_type == OperandTypes.T_EXISTS:
        return skolemize_exists(formula, quantified_varible_list)

    elif formula_type == OperandTypes.T_FORALL:
        return skolemize_forall(formula, quantified_varible_list)

    else:
        raise Exception("Formula of unknown type!")

def skolemize_non_quantifier(formula):
    """Formula that is not quantified is already skolemized. (Prenex assumed)"""
    return copy.deepcopy(formula)

def skolemize_exists(formula, quantified_varible_list):
    """Skolemizes a formula quantified with an existential quantifier."""

    if not quantified_varible_list:
        quantified_variable = formula.get_variable()
        quantified_formula = formula.get_formula()

        return skolemize(quantified_formula.substitute_variable(\
        quantified_variable, ConstantTerm(get_unique_constant())))


def skolemize_forall(formula, quantified_varible_list):
    """Skolemizes a formula quantified with an universal quantifier."""
    pass
