"""Module Herbrand contains Gilmore's algorithm."""
from syntax_tree import OperandTypes, TermTypes, get_unique_constant, \
ConstantTerm, FunctionTerm
from sys import stdout
from itertools import permutations
import pdb

def apply_function(function, operands):
    """Applies a given function to a list of operands.

    Returns a list of all possible function applications."""
    arity = len(function.operands)

    if len(operands) < arity:
        new_operands = list(operands)
        for _ in range(len(operands), arity):
            new_operands += get_unique_constant()
        return [FunctionTerm(function.function_symbol, new_operands)]
    else:
        applications = []
        operand_lists = list(permutations(operands, arity))

        for operand_list in operand_lists:
            applications.append(FunctionTerm(function.function_symbol, \
            operand_list))

        return applications

def fetch_constants(formula):
    """Finds all constants in a formula."""
    formula_type = formula.get_type()
    constants = []

    if formula_type is OperandTypes.T_ATOM \
    or formula_type is TermTypes.T_FUNC:
        for operand in formula.operands:
            constants += fetch_constants(operand)
    elif formula_type is OperandTypes.T_NOT:
        constants = fetch_constants(formula.get_formula())
    elif formula_type is OperandTypes.T_AND or \
    formula_type is OperandTypes.T_OR:
        constants = fetch_constants(formula.get_formula1()) \
        + fetch_constants(formula.get_formula2())
    elif formula_type is TermTypes.T_VAR:
        constants = []
    elif formula_type is TermTypes.T_CONST:
        constants = [formula]
    else:
        raise Exception("Herbrand exception: formula of unexpected type!")

    return remove_duplicates(constants)

def fetch_variables(formula):
    """Finds all variables in a formula."""
    formula_type = formula.get_type()
    variables = []

    if formula_type is OperandTypes.T_ATOM \
    or formula_type is TermTypes.T_FUNC:
        for operand in formula.operands:
            variables += fetch_variables(operand)
    elif formula_type is OperandTypes.T_NOT:
        variables = fetch_variables(formula.get_formula())
    elif formula_type is OperandTypes.T_AND or \
    formula_type is OperandTypes.T_OR:
        variables = fetch_variables(formula.get_formula1()) \
        + fetch_variables(formula.get_formula2())
    elif formula_type is TermTypes.T_VAR:
        variables = [formula]
    elif formula_type is TermTypes.T_CONST:
        variables = []
    else:
        raise Exception("Herbrand exception: formula of unexpected type!")

    return remove_duplicates(variables)


def fetch_functions(formula):
    """Finds all functions in a formula."""
    formula_type = formula.get_type()
    functions = []

    if formula_type is OperandTypes.T_ATOM:
        for operand in formula.operands:
            functions += fetch_functions(operand)
    elif formula_type is OperandTypes.T_NOT:
        functions = fetch_functions(formula.get_formula())
    elif formula_type is OperandTypes.T_AND or \
    formula_type is OperandTypes.T_OR:
        functions = fetch_functions(formula.get_formula1()) \
        + fetch_functions(formula.get_formula2())
    elif formula_type is TermTypes.T_VAR \
    or formula_type is TermTypes.T_CONST:
        functions = []
    elif formula_type is TermTypes.T_FUNC:
        functions = [formula]
    else:
        raise Exception("Herbrand exception: formula of unexpected type!")

    return remove_duplicates(functions)

def remove_duplicates(given_list):
    """Removes duplicates from a given list."""
    without_duplicates = []
    [without_duplicates.append(item) \
    for item in given_list if item not in without_duplicates]

    return without_duplicates

class HerbrandUniverse(object):
    """Class representing a Herbrand Herbrands universe
    of a given formula."""
    level_index = 0

    def __init__(self, formula):
        self.current_universe_level = fetch_constants(formula)
        if not self.current_universe_level:
            self.current_universe_level = [ConstantTerm(get_unique_constant())]
        self.functions = fetch_functions(formula)

    def next_level(self):
        """Returns the next level of the Herbrand universe."""
        self.level_index += 1
        if self.functions:
            self.current_universe_level = remove_duplicates(\
            self.current_universe_level + apply_function(self.functions[0], \
            self.current_universe_level))
        return self.current_universe_level

    def print_current_level(self):
        """Prints the current universe level."""
        stdout.write("H%d: " % self.level_index)
        for item in self.current_universe_level:
            item.print_me()
            stdout.write(" ")
        print

