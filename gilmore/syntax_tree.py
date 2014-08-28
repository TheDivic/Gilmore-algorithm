"""A module that contains the syntax tree for first order logic."""

from sys import stdout
import copy

class OperandTypes(object):
    """An enum for all the operand types in first order logic."""
    T_ATOM = 0
    T_NOT = 1
    T_AND = 2
    T_OR = 3
    T_IMP = 4
    T_IFF = 5
    T_FORALL = 6
    T_EXISTS = 7
    T_TRUE = 8
    T_FALSE = 9

class TermTypes(object):
    """An enum for all the term types in first order logic."""
    T_VAR = 0
    T_FUNC = 1
    T_CONST = 2


class Signature(object):
    """A class that represents a signature in first order logic.

        Signature is a map of FUNCTION => NUM_OF_VARIABLES or PREDICATE => NUM_OF_VARIABLES
        It exists so we can't declare two functions with the same name but the different number of variables,
        or we declare a function that is unkown to our "closed world".
        ( that is not allowed in first order logic ).
    """

    functions = {}
    predicates = {}

    def add_function_symbol(self, function_symbol, arity):
        """Adds a function to the signature."""
        self.functions[function_symbol] = arity

    def add_predicate_symbol(self, predicate_symbol, arity):
        """Adds a predicate to the signature."""
        self.predicates[predicate_symbol] = arity

    def check_function_symbol(self, function_symbol, arity):
        """Returns the arity of a given function symbol."""
        if function_symbol not in self.functions:
            self.functions[function_symbol] = arity
            return True
        elif self.functions[function_symbol] == arity:
            return True
        else:
            return False

    def check_predicate_symbol(self, predicate_symbol, arity):
        """Returns the arity of a given predicate symbol."""
        if predicate_symbol not in self.predicates:
            self.predicates[predicate_symbol] = arity
            return True
        elif self.predicates[predicate_symbol] == arity:
            return True
        else:
            return False

global_signature = Signature()

class VariableTerm:
    """A term that represents a variable, for example p, q, r in formulas like: (p /\\ q) => r"""
    def __init__(self, name):
        self.name = name

    def print_me(self):
        """Print the formula."""
        stdout.write(self.name)

    def get_type(self):
        """Returns the type of this formula."""
        return TermTypes.T_VAR

    def __eq__(self, other):
        """Equality operator."""
        equal = False
        try:
            equal = other.get_type() == TermTypes.T_VAR and self.name == other.name
        except AttributeError ,attr_err:
            print "Exception: %s" % attr_err
            print """-- TIP FROM DIVIC: You probably used substitute_variable with a variable name
instead of a VariableTerm object. --"""
            raise

        return equal

    def __ne__(self):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if self == variable:
            return term
        else:
            return copy.deepcopy(self)

    def contains_variable(self, variable):
        """Checks if this formula contains the given variable."""
        if self == variable:
            return True
        else:
            return False

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        return copy.deepcopy(self)

    def prenex(self):
        """Returns the prenex form of this formula."""
        return copy.deepcopy(self)

class ConstantTerm(object):
    """A term that represents a constant of a given language like: socrat in HUMAN(socrat)."""
    def __init__(self, name):
        self.name = name

    def print_me(self):
        """Prints the formula."""
        stdout.write(self.name)

    def get_type(self):
        """Returns the type of this formula."""
        return TermTypes.T_CONST

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == TermTypes.T_CONST and self.name == other.name

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if self == variable:
            return term
        else:
            return copy.deepcopy(self)

    def contains_variable(self, variable):
        """Checks if this formula contains a given variable."""
        if self == variable:
            return True
        else:
            return False

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        return copy.deepcopy(self)

    def prenex(self):
        """Returns the prenex form of this formula."""
        return copy.deepcopy(self)

class FunctionTerm:
    """A term that represents a function of multiple other terms, for example f(p) or q(x, f(y))."""
    def __init__(self, function_symbol, operands):
        self.function_symbol = function_symbol
        self.operands = operands

        global global_signature

        if not global_signature.check_function_symbol(function_symbol, len(operands)):
            raise Exception("Syntax error! Bad signature.")

    def print_me(self):
        """Prints the formula."""
        stdout.write(self.function_symbol)

        stdout.write("(")
        length = len(self.operands)
        for i in range(0, length - 1):
            self.operands[i].print_me()
            stdout.write(", ")

        self.operands[length-1].print_me()
        stdout.write(")")

    def get_type(self):
        """Returns the type of this formula."""
        return TermTypes.T_FUNC

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == TermTypes.T_FUNC and self.function_symbol == other.function_symbol and self.operands == other.operands

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def contains_variable(self, variable):
        """Checks if this function contains the given variable."""
        for operand in self.operands:
            if operand.contains_variable(variable) == True:
                return True

        return False

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if self.contains_variable(variable):
            temp_ops = []

            for operand in self.operands:
                temp_ops.append(operand.substitute_variable(variable, term))

            return FunctionTerm(self.function_symbol, temp_ops)

        else:
            return copy.deepcopy(self)

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        return copy.deepcopy(self)

    def prenex(self):
        """Return the prenex form of this formula."""
        return copy.deepcopy(self)

class AtomicFormula(object):
    """A class that represents an atomic formula in first order logic, atom, true and false."""
    def nnf(self):
        """Returns the Negation Normal Form of this formula."""
        return copy.deepcopy(self)

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        return copy.deepcopy(self)

    def prenex(self):
        """Returns the prenex form of this formula."""
        return copy.deepcopy(self)


class Atom(AtomicFormula):
    """A class that represents an atom in first order logic.

        Atom is a predicate of multiple terms ( THIS IS DIFFERENT FROM STANDARD ( propositional ) LOGIC ) for example:
        FLIES(bird) is an atom, FLIES is a predicate
        IS_WHOLE_NUMBER(square(whole_number))  is an atom, square() is a function and IS_WHOLE_NUMBER is a predicate.
    """
    def __init__(self, predicate_symbol, operands):
        self.predicate_symbol = predicate_symbol
        self.operands = operands

        global global_signature

        if not global_signature.check_predicate_symbol(predicate_symbol, len(operands)):
            raise Exception("Syntax error! Bad signature")


    def print_me(self):
        """Prints the formula."""
        stdout.write(self.predicate_symbol + "(")

        length = len(self.operands)
        for i in range(0, length - 1):
            self.operands[i].print_me()
            stdout.write(", ")

        self.operands[length-1].print_me()
        stdout.write(")")


    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_ATOM


    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_ATOM and self.predicate_symbol == other.predicate_symbol and self.operands == other.operands

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def contains_variable(self, variable):
        """Checks if this formula contains a given variable."""
        for operand in self.operands:
            if operand.contains_variable(variable) == True:
                return True

        return False


    def substitute_variable(self, variable, term):
        """Substitutes a given variable with a given term."""
        if self.contains_variable(variable):
            temp_ops = []

            for operand in self.operands:
                temp_ops.append(operand.substitute_variable(variable, term))

            return Atom(self.predicate_symbol, temp_ops)

        else:
            return copy.deepcopy(self)


class LogicalConstant(AtomicFormula):
    """A class that represents a logical constant in first order logic."""
    def contains_variable(self, variable):
        """Check if this formula contains a given variable."""
        return False

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        return copy.deepcopy(self)

class TrueConstant(LogicalConstant):
    """A class that represents TRUE."""
    def print_me(self):
        """Prints the formula."""
        stdout.write("TRUE")

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_TRUE

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_TRUE

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)


class FalseConstant(LogicalConstant):
    """A class that represents FALSE."""
    def print_me(self):
        """Prints the formula."""
        stdout.write("FALSE")

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_FALSE

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_FALSE

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

class Not:
    """A class that represents a negation in first order logic."""
    def __init__(self, formula):
        self.formula= formula

    def get_formula(self):
        """Returns the negated formula."""
        return self.formula

    def print_me(self):
        """Prints the formula."""
        stdout.write("(~")
        self.formula.print_me()
        stdout.write(")")

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_NOT

    def nnf(self):
        """Returns the Negation Normal Form of this formula."""

        # DVOSTRUKA NEGACIJA
        if self.formula.get_type() == OperandTypes.T_NOT:
            return self.formula.get_formula().nnf()

        # de Morgan 1: ~( A /\ B) == ~A \/ ~B
        elif self.formula.get_type() == OperandTypes.T_AND:
            not_first = Not(self.formula.get_formula1().nnf())
            not_first = not_first.nnf()

            not_second = Not(self.formula.get_formula2().nnf())
            not_second = not_second.nnf()

            return Or(not_first, not_second)

        # de Morgan 2: ~( A \/ B) == ~A /\ ~B
        elif self.formula.get_type() == OperandTypes.T_OR:
            not_first = Not(self.formula.get_formula1().nnf())
            not_first = not_first.nnf()

            not_second = Not(self.formula.get_formula2().nnf())
            not_second = not_second.nnf()

            return And(not_first, not_second)

        # Negacija implikacije:  ~ ( A ==> B) == A /\ ~B
        elif self.formula.get_type() == OperandTypes.T_IMP:

            first = self.formula.get_formula1().nnf()

            not_second = Not(self.formula.get_formula2().nnf())
            not_second = not_second.nnf()

            return And(first, not_second)

        # Negacija ekvivalencije: ~ ( A <==> B) == ~(A==>B) \/ ~(B==>A)
        elif self.formula.get_type() == OperandTypes.T_IFF:
            formula1 = self.formula.get_formula1().nnf()
            formula2 = self.formula.get_formula2().nnf()

            imp1 = Imp(formula1, formula2)
            imp2 = Imp(formula2, formula1)

            not1 = Not(imp1).nnf()

            not2 = Not(imp2).nnf()

            return Or(not1, not2)

        # ~ FORALL(f) == EXISTS(~f)
        elif self.formula.get_type() == OperandTypes.T_FORALL:
            return Exists(self.formula.get_variable(), Not(self.formula.get_formula()).nnf())

        # ~ EXISTS(f) == FORALL(~f)
        elif self.formula.get_type() == OperandTypes.T_EXISTS:
            return Forall(self.formula.get_variable(), Not(self.formula.get_formula()).nnf())
        else:
            return Not(self.formula.nnf())


    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_NOT and self.formula == other.formula

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def contains_variable(self, variable):
        """Checks if this formula contains the given variable."""
        return self.formula.contains_variable(variable)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if(self.contains_variable(variable)):
            return Not(self.formula.substitute_variable(variable,term))
        else:
            return copy.deepcopy(self)

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        return copy.deepcopy(self)

    def prenex(self):
        """Returns the prenex form of this formula."""
        return copy.deepcopy(self)

class BinaryOperator:
    """A class that represents a binary operator in first order logic."""
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def get_formula1(self):
        """Returns the left conjunct."""
        return self.formula1

    def get_formula2(self):
        """Returns the right conjunct."""
        return self.formula2

    def contains_variable(self, variable):
        """Checks if this formula contains the given variable."""
        return self.formula1.contains_variable(variable) or self.formula2.contains_variable(variable)


class And(BinaryOperator):
    """A class that represents the Conjunction of two formulas in first order logic."""
    def __init__(self, formula1, formula2):
        BinaryOperator.__init__(self, formula1, formula2)

    def print_me(self):
        """Prints the formula."""
        stdout.write("(")
        self.formula1.print_me()
        stdout.write(" /\\ ")
        self.formula2.print_me()
        stdout.write(")")

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_AND

    def nnf(self):
        """Returns the Negation Normal Form of this formula."""
        return And(self.formula1.nnf(), self.formula2.nnf())

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_AND and self.formula1 == other.formula1 and self.formula2 == other.formula2

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if(self.contains_variable(variable)):
            return And(self.formula1.substitute_variable(variable, term), self.formula2.substitute_variable(variable, term))
        else:
            return copy.deepcopy(self)

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex.

            We make the pullquants form using these rules:

                (forall x) A /\\ (forall y) B == (forall z) A /\\ B
                ((exists x) A) /\\ B == (exists z) ( A /\\ B)
                A /\\ (exists x) B == ( exists z) ( A /\\ B)
                ((forall x) A) /\\ B == ( forall z) ( A /\\ B )
                A /\\ (forall x) B == ( forall z ) ( A /\\ B)

            ELSE A /\\ B.
        """
        # (forall x) A /\ (forall y) B == (forall z) A /\ B
        if self.formula1.get_type() == OperandTypes.T_FORALL and self.formula2.get_type() == OperandTypes.T_FORALL:
            #check for special case where x == y
            if self.formula1.variable == self.formula2.variable:
                return Forall(self.formula1.variable, And(self.formula1.formula, self.formula2.formula).pullquants())
            else:
                unique_var = VariableTerm(get_unique_variable())
                new_formula1 = self.formula1.formula.substitute_variable(self.formula1.variable, unique_var)
                new_formula2 = self.formula2.formula.substitute_variable(self.formula2.variable, unique_var)
                return Forall( unique_var, And( new_formula1, new_formula2).pullquants())

        #((exists x) A) /\ B == (exists z) ( A /\ B)
        elif self.formula1.get_type() == OperandTypes.T_EXISTS:
            # if B doesn't contain x then we just pull the quantifier outside
            if self.formula2.contains_variable(self.formula1.variable) == False:
                return Exists(self.formula1.variable, And(self.formula1.formula, self.formula2).pullquants())
            # if B contains x we have to rename x in A
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Exists( unique_var, And(self.formula1.formula.substitute_variable(self.formula1.variable, unique_var), self.formula2).pullquants())

        #A /\ (exists x) B == ( exists z) ( A /\ B)
        elif self.formula2.get_type() == OperandTypes.T_EXISTS:
            # if A doesn't contain x then we just pull the quantifier outside
            if self.formula1.contains_variable(self.formula2.variable) == False:
                return Exists(self.formula2.variable, And(self.formula1 , self.formula2.formula).pullquants())
            # if A contains x we have to rename x in B
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Exists( unique_var, And(self.formula1, self.formula2.formula.substitute_variable(self.formula2.variable, unique_var)).pullquants())
        #((forall x) A) /\ B == ( forall z) ( A /\ B )
        elif self.formula1.get_type() == OperandTypes.T_FORALL:
            # if B doesn't contain x then we just pull the quantifier outside
            if self.formula2.contains_variable(self.formula1.variable) == False:
                return Forall(self.formula1.variable, And(self.formula1.formula, self.formula2).pullquants())
            # if B contains x we have to rename x in A
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Forall( unique_var, And(self.formula1.formula.substitute_variable(self.formula1.variable, unique_var), self.formula2).pullquants())

        #    A /\ (forall x) B == ( forall z ) ( A /\ B)
        elif self.formula2.get_type() == OperandTypes.T_FORALL:
            # if A doesn't contain x then we just pull the quantifier outside
            if self.formula1.contains_variable(self.formula2.variable) == False:
                return Forall(self.formula2.variable, And(self.formula1 , self.formula2.formula).pullquants())
            # if A contains x we have to rename x in B
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Forall( unique_var, And(self.formula1, self.formula2.formula.substitute_variable(self.formula2.variable, unique_var)).pullquants())
        # ELSE A /\ B
        else:
            return copy.deepcopy(self)

    def prenex(self):
        """Returns the prenex form of this formula."""
        return And(self.formula1.prenex(), self.formula2.prenex()).pullquants()

class Or(BinaryOperator):
    """A class that represents the Disjunction of two formulas in first order logic."""
    def __init__(self, formula1, formula2):
        BinaryOperator.__init__(self, formula1, formula2)

    def print_me(self):
        """Prints the formula."""
        stdout.write("(")
        self.formula1.print_me()
        stdout.write(" \\/ ")
        self.formula2.print_me()
        stdout.write(")")

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_OR

    def nnf(self):
        """Returns the Negation Normal Form of this formula."""
        return Or(self.formula1.nnf(), self.formula2.nnf())

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_OR and self.formula1 == other.formula1 and self.formula2 == other.formula2

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if(self.contains_variable(variable)):
            return Or(self.formula1.substitute_variable(variable, term), self.formula2.substitute_variable(variable, term))
        else:
            return copy.deepcopy(self)


    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex.

            We make the pullquants form using these rules:

                (exists x) A \\/ (exists y) B == (exists z) A \\/ B
                ((exists x) A) \\/ B == (exists z) ( A \\/ B)
                A \\/ (exists x) B == ( exists z) ( A \\/ B)
                ((forall x) A) \\/ B == ( forall z) ( A \\/ B )
                A \\/ (forall x) B == ( forall z ) ( A \\/ B)

            ELSE A \\/ B.
        """
        # (exists x) A \/ (exists y) B == (exists z) A \/ B
        if self.formula1.get_type() == OperandTypes.T_EXISTS and self.formula2.get_type() == OperandTypes.T_EXISTS:
            #check for special case where x == y
            if self.formula1.variable == self.formula2.variable:
                return Exists(self.formula1.variable, Or(self.formula1.formula, self.formula2.formula).pullquants())
            else:
                unique_var = VariableTerm(get_unique_variable())
                new_formula1 = self.formula1.formula.substitute_variable(self.formula1.variable, unique_var)
                new_formula2 = self.formula2.formula.substitute_variable(self.formula2.variable, unique_var)
                return Exists( unique_var, Or( new_formula1, new_formula2).pullquants())

        #((exists x) A) \/ B == (exists z) ( A \/ B)
        elif self.formula1.get_type() == OperandTypes.T_EXISTS:
            # if B doesn't contain x then we just pull the quantifier outside
            if self.formula2.contains_variable(self.formula1.variable) == False:
                return Exists(self.formula1.variable, Or(self.formula1.formula, self.formula2).pullquants())
            # if B contains x we have to rename x in A
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Exists( unique_var, Or(self.formula1.formula.substitute_variable(self.formula1.variable, unique_var), self.formula2).pullquants())

        #A \/ (exists x) B == ( exists z) ( A \/ B)
        elif self.formula2.get_type() == OperandTypes.T_EXISTS:
            # if A doesn't contain x then we just pull the quantifier outside
            if self.formula1.contains_variable(self.formula2.variable) == False:
                return Exists(self.formula2.variable, Or(self.formula1 , self.formula2.formula).pullquants())
            # if A contains x we have to rename x in B
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Exists( unique_var, Or(self.formula1, self.formula2.formula.substitute_variable(self.formula2.variable, unique_var)).pullquants())
        #((forall x) A) \/ B == ( forall z) ( A \/ B )
        elif self.formula1.get_type() == OperandTypes.T_FORALL:
            # if B doesn't contain x then we just pull the quantifier outside
            if self.formula2.contains_variable(self.formula1.variable) == False:
                return Forall(self.formula1.variable, Or(self.formula1.formula, self.formula2).pullquants())
            # if B contains x we have to rename x in A
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Forall( unique_var, Or(self.formula1.formula.substitute_variable(self.formula1.variable, unique_var), self.formula2).pullquants())

        #    A \/ (forall x) B == ( forall z ) ( A \/ B)
        elif self.formula2.get_type() == OperandTypes.T_FORALL:
            # if A doesn't contain x then we just pull the quantifier outside
            if self.formula1.contains_variable(self.formula2.variable) == False:
                return Forall(self.formula2.variable, Or(self.formula1, self.formula2.formula).pullquants())
            # if A contains x we have to rename x in B
            else:
                unique_var = VariableTerm(get_unique_variable())
                return Forall(unique_var, Or(self.formula1, self.formula2.formula.substitute_variable(self.formula2.variable, unique_var)).pullquants())
        # ELSE A \/ B
        else:
            return copy.deepcopy(self)


    def prenex(self):
        """Returns the prenex form of this formula."""
        return Or(self.formula1.prenex(), self.formula2.prenex()).pullquants()


class Imp(BinaryOperator):
    """A class that represents the Implication of two formulas in first order logic."""
    def __init__(self, formula1, formula2):
        BinaryOperator.__init__(self, formula1, formula2)

    def print_me(self):
        """Prints the formula."""
        stdout.write("(")
        self.formula1.print_me()
        stdout.write(" ==> ")
        self.formula2.print_me()
        stdout.write(")")

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_IMP

    def nnf(self):
        """Returns the Negation Normal Form of this formula."""
        return Or(Not(self.formula1.nnf()).nnf(), self.formula2.nnf())

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_IMP and self.formula1 == other.formula1 and self.formula2 == other.formula2

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if self.contains_variable(variable):
            return Imp(self.formula1.substitute_variable(variable, term), self.formula2.substitute_variable(variable, term))
        else:
            return copy.deepcopy(self)

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        raise Exception("pullquants failed! Formula must be in nnf!")

    def prenex(self):
        """Returns the prenex form of this formula."""
        raise Exception("prenex failed! Formula must be in nnf!")

class Iff(BinaryOperator):
    """A class that represent the Equivalence of two formulas in first order logic."""
    def __init__(self, formula1, formula2):
        BinaryOperator.__init__(self, formula1, formula2)

    def print_me(self):
        """Prints the formula."""
        stdout.write("(")
        self.formula1.print_me()
        stdout.write(" <==> ")
        self.formula2.print_me()
        stdout.write(")")

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_IFF

    def nnf(self):
        """Returns the Negation Normal Form of this formula."""
        return And(Imp(self.formula1.nnf(), self.formula2.nnf()).nnf(), Imp(self.formula2.nnf(), self.formula1.nnf()).nnf())

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_IFF and self.formula1 == other.formula1 and self.formula2 == other.formula2

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if self.contains_variable(variable):
            return Iff(self.formula1.substitute_variable(variable, term), self.formula2.substitute_variable(variable, term))
        else:
            return copy.deepcopy(self)

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        raise Exception("pullquants failed! Formula must be in nnf!")

    def prenex(self):
        """Returns the prenex form of this formula."""
        raise Exception("prenex failed! Formula must be in nnf!")

class Quantifier(object):
    """A class that represents a quantifier in first order logic."""
    def __init__(self, variable, formula):
        self.variable = variable
        self.formula = formula

    def get_formula(self):
        """Returns the quantified formula."""
        return self.formula

    def get_variable(self):
        """Returns the quantified variable."""
        return self.variable

    def contains_variable(self, variable):
        """Checks if this formula contains a given variable."""
        return self.formula.contains_variable(variable)

class Forall(Quantifier):
    """A class that represents the universal quantifier."""
    def __init__(self, variable, formula):
        Quantifier.__init__(self, variable, formula)

    def print_me(self):
        """Prints the formula."""
        stdout.write("(A{")
        self.variable.print_me()
        stdout.write("}.(")
        self.formula.print_me()
        stdout.write(")")

    def nnf(self):
        """Returns the Negation Normal Form of this formula."""
        return Forall(self.variable, self.formula.nnf())

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_FORALL

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_FORALL and self.variable == other.variable and self.formula == other.formula

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if self.variable == variable:
            return copy.deepcopy(self)

        if term.contains_variable(self.variable):
            unique_var = VariableTerm(get_unique_variable())
            new_formula = self.formula.substitute_variable(self.variable, unique_var)
            return Forall(unique_var, new_formula.substitute_variable(variable, term))

        else:
            return Forall(self.variable, self.formula.substitute_variable(variable, term))

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        return copy.deepcopy(self)

    def prenex(self):
        """Returns the prenex form of this formula."""
        return Forall(self.variable, self.formula.prenex())

class Exists(Quantifier):
    """A class that represents the existential quantifier."""
    def __init__(self, variable, formula):
        Quantifier.__init__(self, variable, formula)

    def print_me(self):
        """Prints the formula."""
        stdout.write("(E{")
        self.variable.print_me()
        stdout.write("}.(")
        self.formula.print_me()
        stdout.write(")")

    def nnf(self):
        """Returns the Negation Normal Form of this formula."""
        return Exists(self.variable, self.formula.nnf())

    def get_type(self):
        """Returns the type of this formula."""
        return OperandTypes.T_EXISTS

    def __eq__(self, other):
        """Equality operator."""
        return other.get_type() == OperandTypes.T_EXISTS and self.variable == other.variable and self.formula == other.formula

    def __ne__(self, other):
        """Non-equality operator."""
        return not self.__eq__(other)

    def substitute_variable(self, variable, term):
        """Substitutes the given variable with a given term."""
        if self.variable == variable:
            return copy.deepcopy(self)

        if term.contains_variable(self.variable):
            unique_var = VariableTerm(get_unique_variable())
            new_formula = self.formula.substitute_variable(self.variable, unique_var)
            return Exists(unique_var, new_formula.substitute_variable(variable, term))

        else:
            return Exists(self.variable, self.formula.substitute_variable(variable, term))

    def pullquants(self):
        """Pulls the quantifiers in front of the formula, for prenex."""
        return copy.deepcopy(self)

    def prenex(self):
        """Returns the prenex form of this formula."""
        return Exists(self.variable, self.formula.prenex())


#unique variable index
uv_index = 0
#unique constant index
uc_index = 0
#unique function index
uf_index = 0

def get_unique_variable():
    """Returns an unique variable."""
    global uv_index
    uv_index = uv_index + 1
    return "uv%d" % uv_index

def get_unique_constant():
    """Returns an unique constant."""
    global uc_index
    uc_index = uc_index + 1
    return "uc%d" % uc_index

def get_unique_function(operands):
    """Returns an unique function."""
    global uf_index
    uf_index = uf_index + 1
    return FunctionTerm("uf%d" % uf_index, operands)
