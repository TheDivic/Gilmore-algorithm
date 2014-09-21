"""Module dnf that contains the functions for the Disjunctive Normal Form"""
from syntax_tree import OperandTypes
from sys import stdout

#Types that are already in DNF
ATOMIC_TYPES = [OperandTypes.T_ATOM, OperandTypes.T_NOT]

def print_dnf(clause_list):
    """Prints the clause list."""
    for clause in clause_list:
        stdout.write("(")
        for i in range(0, len(clause) - 1):
            clause[i].print_me()
            stdout.write(" /\\ ")
        clause[len(clause)-1].print_me()
        stdout.write(")")
        print

def dnf(formula):
    """Transforms a formula that is in prenex form without quantifiers
    into its Disjunctive Normal Form"""
    formula_type = formula.get_type()
    if formula_type in ATOMIC_TYPES:
        return [formula]
    elif formula_type is OperandTypes.T_OR:
        return dnf(formula.get_formula1()) + dnf(formula.get_formula2())
    elif formula_type is OperandTypes.T_AND:
        return make_pairs(dnf(formula.get_formula1()), \
        dnf(formula.get_formula2()))
    else:
        raise Exception("DNF exception: given formula must be in NNF, \
        without quantifiers.")


def make_pairs(atom_list1, atom_list2):
    """Cartesian product of two lists."""
    return [(x, y) for x in atom_list1 for y in atom_list2]



