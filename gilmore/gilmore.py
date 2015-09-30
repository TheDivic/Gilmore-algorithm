"""Gilmore's algorithm implementation."""

from syntax_tree import And, OperandTypes, Not
from skolemize import skolemize, eliminate_universal_quantifiers
from herbrand import HerbrandUniverse, fetch_variables
from dnf import dnf, print_dnf
from itertools import product
import pdb

GILMORE_LIMIT = 5

def prove_valid(formula):
    not_formula = Not(formula)
    go_gilmore(not_formula)

def go_gilmore(formula):
    """Gilmore's algorithm implementation."""

    #Transform the formula into its prenex form
    #and eliminate the universal quantifiers
    transformed_formula = formula.nnf()
    transformed_formula = transformed_formula.prenex()
    transformed_formula = skolemize(transformed_formula, [])
    transformed_formula = eliminate_universal_quantifiers(transformed_formula)

    print "-- TRANSFORMED FORMULA --"
    transformed_formula.print_me()
    print

    universe = HerbrandUniverse(transformed_formula)
    variables = fetch_variables(transformed_formula)

    current_level = universe.get_current_level()
    num_vars = len(variables)

    # ALGORITHM STARTS HERE: iterates until the proof is found
    # or we have reached the GILMORE_LIMIT
    for iteration in range(0, GILMORE_LIMIT):
        print("Iteration number %s" %(iteration + 1))
        substitutions = list(product(current_level, repeat=num_vars))
        subd_formula = transformed_formula

        for i in range(0, num_vars):
            subd_formula = subd_formula.substitute_variable(variables[i],\
            substitutions[0][i])

        transformed_formula.print_me()
        print

        for i in range(1, len(substitutions)):
            new_subd_formula = transformed_formula
            for j in range(0, num_vars):
                new_subd_formula = new_subd_formula.substitute_variable(\
                variables[j], substitutions[i][j])

            subd_formula = And(subd_formula, new_subd_formula)

        print "-- SUBD FORMULA --"
        subd_formula.print_me()
        print
        print "-- DNF WITH SUBSTITUTIONS --"
        dnf_formula = dnf(subd_formula)
        print_dnf(dnf_formula)
        print "---------"

        remove_count = 0

        # MULTIPLICATION METHOD
        for clause in dnf_formula:
            found_positive = []
            found_negative = []
            found = False

            for literal in clause:
                if literal.get_type() is OperandTypes.T_NOT:
                    if literal.get_formula() in found_positive:
                        found = True
                        remove_count += 1
                        break
                    else:
                        found_negative.append(literal.get_formula())
                elif literal.get_type() is OperandTypes.T_ATOM:
                    if literal in found_negative:
                        found = True
                        remove_count += 1
                        break
                    else:
                        found_positive.append(literal)
                else:
                    raise Exception("Gilmore multiplication method exception!")

            if not found:
                print("NOT ELIMINATED")
                print("["),
                for literal in clause:
                    literal.print_me()
                    print(", "),
                print("]")

        print("REMOVE COUNT: %s" %remove_count)
        if remove_count == len(dnf_formula):
            print "UNSAT!"
            break
        else:
            print "Next level."

        current_level = universe.next_level()

    if iteration is GILMORE_LIMIT - 1:
        print "Proof not found."
