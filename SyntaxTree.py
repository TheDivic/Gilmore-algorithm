from sys import stdout
import copy

# Enum for all possible types of operands
class OperandTypes:
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

# Enum for all possible term types
class TermTypes:
	T_VAR = 0
	T_FUNC = 1
	T_CONST = 2

uv_index=0

def getUniqueVariable():
	global uv_index
	uv_index = uv_index + 1
	return "uv%d" % uv_index


# Signature is a map of FUNCTION => NUM_OF_VARIABLES or PREDICATE => NUM_OF_VARIABLES
# It exists so we can't declare two functions with the same name but the different number of variables,
# or we declare a function that is unkown to our "closed world".
# ( that is not allowed in first order logic )
class Signature:
	functions = {}
	predicates = {}

	def addFunctionSymbol(self, functionSymbol, arity):
		self.functions[functionSymbol] = arity

	def addPredicateSymbol(self, predicateSymbol, arity):
		self.predicates[predicateSymbol] = arity

	def checkFunctionSymbol(self, functionSymbol):
		if functionSymbol in self.functions:
			return self.functions[functionSymbol]
		else:
			return False	

	def checkPredicateSymbol(self, predicateSymbol):
		if predicateSymbol in self.predicates:
			return self.predicates[predicateSymbol]
		else:
			return False		

	

# A term that represents a variable, for example p, q, r in formulas like: (p /\ q) => r
class VariableTerm:

	def __init__(self, name):
		self.name = name

	def printMe(self):
		stdout.write(self.name)	

	def getType(self):
		return TermTypes.T_VAR	

	def __eq__(self, other):
		return other.getType() == TermTypes.T_VAR and self.name == other.name	

	def __ne__(self):
		return not self.__eq__(other)

	def substituteVariable(self, variable, term):
		if self == variable:
			return term
		else:
			return copy.deepcopy(self)		

	def containsVariable(self, variable):
		if self == variable:
			return True
		else:
			return False	

	def pullQuants(self):
		return copy.deepcopy(self)		

	def prenex(self):
		return copy.deepcopy(self)

# A term that represents a constant of a given language like: socrat in HUMAN(socrat)
class ConstantTerm:		

	def __init__(self, name):
		self.name = name

	def printMe(self):
		stdout.write(self.name)

	def getType(self):
		return TermTypes.T_CONST		

	def __eq__(self, other):
		return other.getType() == TermTypes.T_CONST and self.name == other.name	

	def __ne__(self):
		return not self.__eq__(other)	

	def substituteVariable(self, variable, term):
		if self == variable:
			return term
		else:
			return copy.deepcopy(self)		

	def containsVariable(self, variable):
		if self == variable:
			return True
		else:
			return False	

	def pullQuants(self):
		return copy.deepcopy(self)	

	def prenex(self):
		return copy.deepcopy(self)				

# A term that represents a function of multiple other terms, for example f(p) or q(x, f(y)) 	
class FunctionTerm:
	def __init__(self, signature, functionSymbol, operands):
		self.signature = signature
		self.functionSymbol = functionSymbol
		self.operands = operands

		check = signature.checkFunctionSymbol(functionSymbol)

		if check is False or check!=len(operands):
			raise Exception("Syntax error! Bad signature.")

	def printMe(self):
		stdout.write(self.functionSymbol)

		stdout.write("(")
		length = len(self.operands)
		for i in range(0, length - 1):
			self.operands[i].printMe()
			stdout.write(", ")

		self.operands[length-1].printMe()
		stdout.write(")")

	def getType(self):
		return TermTypes.T_FUNC	

	def __eq__(self, other):
		return other.getType() == TermTypes.T_FUNC and self.functionSymbol == other.functionSymbol and self.operands == other.operands

	def __ne__(self, other):
		return not self.__eq__(other)

	def containsVariable(self, variable):
		for op in self.operands:
			if op.containsVariable(variable) == True:
				return True

		return False		

	def substituteVariable(self, variable, term):	
		if self.containsVariable(variable):
			temp_ops = []

			for op in self.operands:
				temp_ops.append(op.substituteVariable(variable,term))

			return FunctionTerm(self.signature, self.functionSymbol, temp_ops)	

		else:
			return copy.deepcopy(self)	
				
	def pullQuants(self):
		return copy.deepcopy(self)			

	def prenex(self):
		return copy.deepcopy(self)	

# Atomic formulas: atom, true and false
class AtomicFormula:
	def NNF(self):
		return copy.deepcopy(self)

	def pullQuants(self):
		return copy.deepcopy(self)	

	def prenex(self):
		return copy.deepcopy(self)

# Atom is a predicate of multiple terms ( THIS IS DIFFERENT FROM STANDARD ( propositional ) LOGIC ) for example:
# FLIES(bird) is an atom, FLIES is a predicate 
# IS_WHOLE_NUMBER(square(whole_number))  is an atom, square() is a function and IS_WHOLE_NUMBER is a predicate
class Atom(AtomicFormula):
	def __init__(self, signature, predicateSymbol, operands):
		self.signature = signature
		self.predicateSymbol = predicateSymbol
		self.operands = operands

		check = signature.checkPredicateSymbol(predicateSymbol)

		if check is False or check!=len(operands):
			raise Exception("Syntax error! Bad signature")


	def printMe(self):
		stdout.write(self.predicateSymbol + "(")

		length = len(self.operands)
		for i in range(0, length - 1):
			self.operands[i].printMe()
			stdout.write(", ")

		self.operands[length-1].printMe()
		stdout.write(")")
			

	def getType(self):
		return OperandTypes.T_ATOM	


	def __eq__(self, other):
		return other.getType() == OperandTypes.T_ATOM and self.predicateSymbol == other.predicateSymbol and self.operands == other.operands	

	def __ne__(self, other):
		return not self.__eq__(other)	


	def containsVariable(self, variable):
		for op in self.operands:
			if op.containsVariable(variable) == True:
				return True

		return False	


	def substituteVariable(self, variable, term):	
		if self.containsVariable(variable):
			temp_ops = []

			for op in self.operands:
				temp_ops.append(op.substituteVariable(variable,term))

			return Atom(self.signature, self.predicateSymbol, temp_ops)	

		else:
			return copy.deepcopy(self)	


class LogicalConstant(AtomicFormula):
	def containsVariable(self, variable):
		return False

	def substituteVariable(self, variable, term):
		return copy.deepcopy(self)	

#TRUE
class TrueConstant(LogicalConstant):
	def printMe(self):
		stdout.write("TRUE")

	def getType(self):
		return OperandTypes.T_TRUE

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_TRUE

	def __ne__(self, other):
		return not self.__eq__(other)		


#FALSE
class FalseConstant(LogicalConstant):
	def printMe(self):
		stdout.write("FALSE")

	def getType(self):
		return OperandTypes.T_FALSE

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_FALSE

	def __ne__(self, other):
		return not self.__eq__(other)


# Negation of a formula
class Not:
	def __init__(self, formula):
		self.formula= formula

	def getFormula(self):
		return self.formula

	def printMe(self):
		stdout.write("(~")
		self.formula.printMe()
		stdout.write(")")	

	def getType(self):
		return OperandTypes.T_NOT	

	def NNF(self):

		# DVOSTRUKA NEGACIJA
		if self.formula.getType() == OperandTypes.T_NOT:
			return self.formula.getFormula().NNF()

		# de Morgan 1: ~( A /\ B) == ~A \/ ~B
		elif self.formula.getType() == OperandTypes.T_AND:	
			notFirst = Not(self.formula.getFormula1().NNF())
			notFirst = notFirst.NNF()

			notSecond = Not(self.formula.getFormula2().NNF())
			notSecond = notSecond.NNF()

			return Or(notFirst, notSecond)

		# de Morgan 2: ~( A \/ B) == ~A /\ ~B	
		elif self.formula.getType() == OperandTypes.T_OR:	
			notFirst = Not(self.formula.getFormula1().NNF())
			notFirst = notFirst.NNF()

			notSecond = Not(self.formula.getFormula2().NNF())
			notSecond = notSecond.NNF()

			return And(notFirst, notSecond) 	

		# Negacija implikacije:  ~ ( A ==> B) == A /\ ~B
		elif self.formula.getType() == OperandTypes.T_IMP:	

			first = self.formula.getFormula1().NNF()

			notSecond = Not(self.formula.getFormula2().NNF())
			notSecond = notSecond.NNF()

			return And(first, notSecond)

		# Negacija ekvivalencije: ~ ( A <==> B) == ~(A==>B) \/ ~(B==>A)
		elif self.formula.getType() == OperandTypes.T_IFF:
			formula1 = self.formula.getFormula1().NNF()
			formula2 = self.formula.getFormula2().NNF()

			imp1 = Imp(formula1, formula2)
			imp2 = Imp(formula2, formula1)

			not1 = Not(imp1).NNF()

			not2 = Not(imp2).NNF()

			return Or(not1, not2)

		# ~ FORALL(f) == EXISTS(~f)
		elif self.formula.getType() == OperandTypes.T_FORALL:
			return Exists(self.formula.getVariable(), Not(self.formula.getFormula()).NNF())

		# ~ EXISTS(f) == FORALL(~f)
		elif self.formula.getType() == OperandTypes.T_EXISTS:
			return Forall(self.formula.getVariable(), Not(self.formula.getFormula()).NNF())
		else:
			return Not(self.formula.NNF())	


	def __eq__(self, other):
		return other.getType() == OperandTypes.T_NOT and self.formula == other.formula

	def __ne__(self, other):
		return not self.__eq__(other)		

	def containsVariable(self, variable):
		return self.formula.containsVariable(variable)

	def substituteVariable(self, variable, term):
		if(self.containsVariable(variable)):
			return Not(self.formula.substituteVariable(variable,term))
		else:
			return copy.deepcopy(self)	
		
	def pullQuants(self):
		return copy.deepcopy(self)	

	def prenex(self):
		return copy.deepcopy(self)

# Binary operator
class BinaryOperator:

	def __init__(self, formula1, formula2):
		self.formula1 = formula1
		self.formula2 = formula2

	def getFormula1(self):
		return self.formula1

	def getFormula2(self):
		return self.formula2		

	def containsVariable(self, variable):	
		return self.formula1.containsVariable(variable) or self.formula2.containsVariable(variable)


# Conjunction of two formulas 
class And(BinaryOperator):

	def __init__(self, formula1, formula2):
		BinaryOperator.__init__(self, formula1, formula2)

	def printMe(self):
		stdout.write("(")
		self.formula1.printMe()
		stdout.write(" /\\ ")
		self.formula2.printMe()
		stdout.write(")")

	def getType(self):
		return OperandTypes.T_AND	

	def NNF(self):
		return And(self.formula1.NNF(), self.formula2.NNF())	

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_AND and self.formula1 == other.formula1 and self.formula2 == other.formula2

	def __ne__(self, other):
		return not self.__eq__(other)	

	def substituteVariable(self, variable, term):
		if(self.containsVariable(variable)):
			return And(self.formula1.substituteVariable(variable, term), self.formula2.substituteVariable(variable, term))
		else:
			return copy.deepcopy(self)		

	# We make the pullQuants form using these rules:
	#
	#    (forall x) A /\ (forall y) B == (forall z) A /\ B
	#	 ((exists x) A) /\ B == (exists z) ( A /\ B)
	#	 A /\ (exists x) B == ( exists z) ( A /\ B)
	#	 ((forall x) A) /\ B == ( forall z) ( A /\ B )
	#	 A /\ (forall x) B == ( forall z ) ( A /\ B)
	#
	# ELSE A /\ B
	def pullQuants(self):		

		# (forall x) A /\ (forall y) B == (forall z) A /\ B
		if self.formula1.getType() == OperandTypes.T_FORALL and self.formula2.getType() == OperandTypes.T_FORALL:
			#check for special case where x == y
			if self.formula1.variable == self.formula2.variable:
				return Forall(self.formula1.variable, And(self.formula1.formula, self.formula2.formula).pullQuants())
			else:
				unique_var = VariableTerm(getUniqueVariable())
				new_formula1 = self.formula1.formula.substituteVariable(self.formula1.variable, unique_var)
				new_formula2 = self.formula2.formula.substituteVariable(self.formula2.variable, unique_var)				
				return Forall( unique_var, And( new_formula1, new_formula2).pullQuants())

		#((exists x) A) /\ B == (exists z) ( A /\ B)		
		elif self.formula1.getType() == OperandTypes.T_EXISTS:
			# if B doesn't contain x then we just pull the quantifier outside
			if self.formula2.containsVariable(self.formula1.variable) == False:
				return Exists(self.formula1.variable, And(self.formula1.formula, self.formula2).pullQuants())	
			# if B contains x we have to rename x in A
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Exists( unique_var, And(self.formula1.formula.substituteVariable(self.formula1.variable, unique_var), self.formula2).pullQuants())	
		
		#A /\ (exists x) B == ( exists z) ( A /\ B)		
		elif self.formula2.getType() == OperandTypes.T_EXISTS:
			# if A doesn't contain x then we just pull the quantifier outside
			if self.formula1.containsVariable(self.formula2.variable) == False:
				return Exists(self.formula2.variable, And(self.formula1 , self.formula2.formula).pullQuants())	
			# if A contains x we have to rename x in B
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Exists( unique_var, And(self.formula1, self.formula2.formula.substituteVariable(self.formula2.variable, unique_var)).pullQuants())	
		#((forall x) A) /\ B == ( forall z) ( A /\ B )
		elif self.formula1.getType() == OperandTypes.T_FORALL:
			# if B doesn't contain x then we just pull the quantifier outside
			if self.formula2.containsVariable(self.formula1.variable) == False:
				return Forall(self.formula1.variable, And(self.formula1.formula, self.formula2).pullQuants())	
			# if B contains x we have to rename x in A
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Forall( unique_var, And(self.formula1.formula.substituteVariable(self.formula1.variable, unique_var), self.formula2).pullQuants())	
			
		#	 A /\ (forall x) B == ( forall z ) ( A /\ B)	
		elif self.formula2.getType() == OperandTypes.T_FORALL:
			# if A doesn't contain x then we just pull the quantifier outside
			if self.formula1.containsVariable(self.formula2.variable) == False:
				return Forall(self.formula2.variable, And(self.formula1 , self.formula2.formula).pullQuants())	
			# if A contains x we have to rename x in B
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Forall( unique_var, And(self.formula1, self.formula2.formula.substituteVariable(self.formula2.variable, unique_var)).pullQuants())	
		# ELSE A /\ B
		else:
			return copy.deepcopy(self)

	def prenex(self):
		f1 = self.formula1.prenex()
		f2 = self.formula2.prenex()

		return And(f1, f2).pullQuants()		

# Disjunction of two formulas
class Or(BinaryOperator):
	def __init__(self, formula1, formula2):
		BinaryOperator.__init__(self, formula1, formula2)

	def printMe(self):
		stdout.write("(")
		self.formula1.printMe()
		stdout.write(" \\/ ")
		self.formula2.printMe()
		stdout.write(")")

	def getType(self):
		return OperandTypes.T_OR

	def NNF(self):
		return Or(self.formula1.NNF(), self.formula2.NNF())		

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_OR and self.formula1 == other.formula1 and self.formula2 == other.formula2

	def __ne__(self, other):
		return not self.__eq__(other)		

	def substituteVariable(self, variable, term):
		if(self.containsVariable(variable)):
			return Or(self.formula1.substituteVariable(variable, term), self.formula2.substituteVariable(variable, term))
		else:
			return copy.deepcopy(self)	

	# We make the pullQuants form using these rules:
	#
	#    (exists x) A \/ (exists y) B == (exists z) A \/ B
	#	 ((exists x) A) \/ B == (exists z) ( A \/ B)
	#	 A \/ (exists x) B == ( exists z) ( A \/ B)
	#	 ((forall x) A) \/ B == ( forall z) ( A \/ B )
	#	 A \/ (forall x) B == ( forall z ) ( A \/ B)
	#
	# ELSE A \/ B
	def pullQuants(self):		

		# (exists x) A \/ (exists y) B == (exists z) A \/ B
		if self.formula1.getType() == OperandTypes.T_EXISTS and self.formula2.getType() == OperandTypes.T_EXISTS:
			#check for special case where x == y
			if self.formula1.variable == self.formula2.variable:
				return Exists(self.formula1.variable, Or(self.formula1.formula, self.formula2.formula).pullQuants())
			else:
				unique_var = VariableTerm(getUniqueVariable())
				new_formula1 = self.formula1.formula.substituteVariable(self.formula1.variable, unique_var)
				new_formula2 = self.formula2.formula.substituteVariable(self.formula2.variable, unique_var)				
				return Exists( unique_var, Or( new_formula1, new_formula2).pullQuants())

		#((exists x) A) \/ B == (exists z) ( A \/ B)		
		elif self.formula1.getType() == OperandTypes.T_EXISTS:
			# if B doesn't contain x then we just pull the quantifier outside
			if self.formula2.containsVariable(self.formula1.variable) == False:
				return Exists(self.formula1.variable, Or(self.formula1.formula, self.formula2).pullQuants())	
			# if B contains x we have to rename x in A
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Exists( unique_var, Or(self.formula1.formula.substituteVariable(self.formula1.variable, unique_var), self.formula2).pullQuants())	
		
		#A \/ (exists x) B == ( exists z) ( A \/ B)		
		elif self.formula2.getType() == OperandTypes.T_EXISTS:
			# if A doesn't contain x then we just pull the quantifier outside
			if self.formula1.containsVariable(self.formula2.variable) == False:
				return Exists(self.formula2.variable, Or(self.formula1 , self.formula2.formula).pullQuants())	
			# if A contains x we have to rename x in B
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Exists( unique_var, Or(self.formula1, self.formula2.formula.substituteVariable(self.formula2.variable, unique_var)).pullQuants())	
		#((forall x) A) \/ B == ( forall z) ( A \/ B )
		elif self.formula1.getType() == OperandTypes.T_FORALL:
			# if B doesn't contain x then we just pull the quantifier outside
			if self.formula2.containsVariable(self.formula1.variable) == False:
				return Forall(self.formula1.variable, Or(self.formula1.formula, self.formula2).pullQuants())	
			# if B contains x we have to rename x in A
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Forall( unique_var, Or(self.formula1.formula.substituteVariable(self.formula1.variable, unique_var), self.formula2).pullQuants())	
			
		#	 A \/ (forall x) B == ( forall z ) ( A \/ B)	
		elif self.formula2.getType() == OperandTypes.T_FORALL:
			# if A doesn't contain x then we just pull the quantifier outside
			if self.formula1.containsVariable(self.formula2.variable) == False:
				return Forall(self.formula2.variable, Or(self.formula1 , self.formula2.formula).pullQuants())	
			# if A contains x we have to rename x in B
			else:
				unique_var = VariableTerm(getUniqueVariable())
				return Forall( unique_var, Or(self.formula1, self.formula2.formula.substituteVariable(self.formula2.variable, unique_var)).pullQuants())	
		# ELSE A \/ B
		else:
			return copy.deepcopy(self)	


	def prenex(self):
		f1 = self.formula1.prenex()
		f2 = self.formula2.prenex()

		return Or(f1, f2).pullQuants()


# Implication of two formulas
class Imp(BinaryOperator):
	def __init__(self, formula1, formula2):
		BinaryOperator.__init__(self, formula1, formula2)

	def printMe(self):
		stdout.write("(")
		self.formula1.printMe()
		stdout.write(" ==> ")
		self.formula2.printMe()
		stdout.write(")")

	def getType(self):
		return OperandTypes.T_IMP

	def NNF(self):
		return Or(Not(self.formula1.NNF()).NNF(), self.formula2.NNF())	

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_IMP and self.formula1 == other.formula1 and self.formula2 == other.formula2

	def __ne__(self, other):
		return not self.__eq__(other)	

	def substituteVariable(self, variable, term):
		if(self.containsVariable(variable)):
			return Imp(self.formula1.substituteVariable(variable, term), self.formula2.substituteVariable(variable, term))
		else:
			return copy.deepcopy(self)	

	def pullQuants(self):
		raise Exception("pullQuants failed! Formula must be in NNF!")				

	def prenex(self):
		raise Exception("prenex failed! Formula must be in NNF!")

# Equivalence of two formulas
class Iff(BinaryOperator):
	def __init__(self, formula1, formula2):
		BinaryOperator.__init__(self, formula1, formula2)

	def printMe(self):
		stdout.write("(")
		self.formula1.printMe()
		stdout.write(" <==> ")
		self.formula2.printMe()
		stdout.write(")")

	def getType(self):
		return OperandTypes.T_IFF

	def NNF(self):
		return And(Imp(self.formula1.NNF(), self.formula2.NNF()).NNF(), Imp(self.formula2.NNF(), self.formula1.NNF()).NNF())	

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_IFF and self.formula1 == other.formula1 and self.formula2 == other.formula2

	def __ne__(self, other):
		return not self.__eq__(other)	

	def substituteVariable(self, variable, term):
		if(self.containsVariable(variable)):
			return Iff(self.formula1.substituteVariable(variable, term), self.formula2.substituteVariable(variable, term))
		else:
			return copy.deepcopy(self)		

	def pullQuants(self):
		raise Exception("pullQuants failed! Formula must be in NNF!")		

	def prenex(self):
		raise Exception("prenex failed! Formula must be in NNF!")

class Quantifier:
	def __init__(self, variable, formula):
		self.variable = variable
		self.formula = formula

	def getFormula(self):
		return self.formula

	def getVariable(self):
		return self.variable	

	def containsVariable(self, variable):	
		return self.formula.containsVariable(variable)

# Universal quantifier
class Forall(Quantifier):
	def __init__(self, variable, formula):
		Quantifier.__init__(self, variable, formula)		

	def printMe(self):
		stdout.write("(A{")
		self.variable.printMe()
		stdout.write("}.(")
		self.formula.printMe()	
		stdout.write(")")	

	def NNF(self):
		return Forall(self.variable, self.formula.NNF())

	def getType(self):
		return OperandTypes.T_FORALL	

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_FORALL and self.variable == other.variable and self.formula == other.formula

	def __ne__(self, other):
		return not self.__eq__(other)	

	def substituteVariable(self, variable, term):
		if self.variable == variable:
			return copy.deepcopy(self)

		if(term.containsVariable(self.variable)):
			unique_var = VariableTerm(getUniqueVariable())
			new_formula = self.formula.substituteVariable(self.variable, unique_var)
			return Forall(unique_var, new_formula.substituteVariable(variable, term))

		else:
			return Forall(self.variable, self.formula.substituteVariable(variable, term))	

	def pullQuants(self):
		return copy.deepcopy(self)
		
	def prenex(self):
		return Forall(self.variable, self.formula.prenex())	

# Existential quantifier
class Exists(Quantifier):
	def __init__(self, variable, formula):
		Quantifier.__init__(self, variable, formula)		

	def printMe(self):
		stdout.write("(E{")
		self.variable.printMe()
		stdout.write("}.(")
		self.formula.printMe()	
		stdout.write(")")	

	def NNF(self):
		return Exists(self.variable, self.formula.NNF())	

	def getType(self):
		return OperandTypes.T_EXISTS	

	def __eq__(self, other):
		return other.getType() == OperandTypes.T_EXISTS and self.variable == other.variable and self.formula == other.formula

	def __ne__(self, other):
		return not self.__eq__(other)	

	def substituteVariable(self, variable, term):
		
		if self.variable == variable:
			return copy.deepcopy(self)

		if(term.containsVariable(self.variable)):
			unique_var = VariableTerm(getUniqueVariable())
			new_formula = self.formula.substituteVariable(self.variable, unique_var)
			return Exists(unique_var, new_formula.substituteVariable(variable, term))

		else:
			return Exists(self.variable, self.formula.substituteVariable(variable, term))	

	def pullQuants(self):
		return copy.deepcopy(self)		

	def prenex(self):
		return Exists(self.variable, self.formula.prenex())		
