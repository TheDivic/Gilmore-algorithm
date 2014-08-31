"""A module that contains the Skolemize function.

Skolemization eliminates the existential quantifiers from the formula."""
import copy
from syntax_tree import OperandTypes, get_unique_constant,\
ConstantTerm, Forall, get_unique_function

# Non-quantifier operand types
NOT_QUANTIFIERS = [OperandTypes.T_ATOM, OperandTypes.T_NOT,\
    OperandTypes.T_AND, OperandTypes.T_OR, OperandTypes.T_IMP, \
    OperandTypes.T_IFF]

def skolemize(formula, quantified_varible_list):
    """Skolemizes (eliminates the existential quantifiers) the given formula.

        We assume that the formula is in the prenex  form.
    """
    formula_type = formula.get_type()

    if formula_type in NOT_QUANTIFIERS:
        return skolemize_non_quantifier(formula)

    elif formula_type == OperandTypes.T_EXISTS:
        return skolemize_exists(formula, quantified_varible_list)

    elif formula_type == OperandTypes.T_FORALL:
        return skolemize_forall(formula, quantified_varible_list)

    else:
        raise Exception("Skolemize exception: formula must be in nnf, \
        prenex form!")

def skolemize_non_quantifier(formula):
    """Formula that is not quantified is already skolemized. (Prenex assumed)"""
    return copy.deepcopy(formula)

def skolemize_exists(formula, quantified_varible_list):
    """Skolemizes a formula quantified with an existential quantifier."""
    quantified_variable = formula.get_variable()
    quantified_formula = formula.get_formula()

    if not quantified_varible_list:
        return skolemize(quantified_formula.substitute_variable(\
        quantified_variable, ConstantTerm(get_unique_constant())), \
        quantified_varible_list)
    else:
        new_function = get_unique_function(quantified_varible_list)
        return skolemize(quantified_formula.substitute_variable(\
        quantified_variable, new_function), quantified_varible_list)


def skolemize_forall(formula, quantified_varible_list):
    """Skolemizes a formula quantified with an universal quantifier."""
    quantified_variable = formula.get_variable()
    quantified_formula = formula.get_formula()

    if not quantified_varible_list:
        quantified_varible_list = [quantified_variable]
    else:
        quantified_varible_list.append(quantified_variable)
    return Forall(quantified_variable, skolemize(quantified_formula, \
        quantified_varible_list))

def eliminate_universal_quantifiers(formula):
    """Eliminates the universal quantifers from a skolemized formula."""
    formula_type = formula.get_type()

    if formula_type in NOT_QUANTIFIERS:
        return copy.deepcopy(formula)
    elif formula_type == OperandTypes.T_FORALL:
        return eliminate_universal_quantifiers(formula.get_formula())
    else:
        raise Exception("Eliminate quantifiers exception: \
        formula of unexpected type!")


