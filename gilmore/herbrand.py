"""Module Herbrand contains Gilmore's algorithm."""
from syntax_tree import OperandTypes, TermTypes, get_unique_constant, \
ConstantTerm
from sys import stdout

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

    return constants


def fetch_functions(formula):
    """Finds all functions in a formula."""
    return []

def remove_duplicates(given_list):
    """Removes duplicates from a given list."""
    without_duplicates = []
    duplicate_filter = [without_duplicates.append(item) \
    for item in given_list if item not in without_duplicates]

    return without_duplicates

class HerbrandUniverse(object):
    """Class representing a Herbrand Herbrands universe
    of a given formula."""
    level_index = 0

    def __init__(self, formula):
        self.current_universe_level = remove_duplicates(fetch_constants(formula))
        if not self.current_universe_level:
            self.current_universe_level = [ConstantTerm(get_unique_constant())]
        self.functions = fetch_functions(formula)

    def next_level(self):
        """Returns the next level of the Herbrand universe."""
        self.level_index += 1
        return self.current_universe_level

    def print_current_level(self):
        """Prints the current universe level."""
        stdout.write("H%d: " % self.level_index)
        for item in self.current_universe_level:
            item.print_me()
            stdout.write(" ")
        print

