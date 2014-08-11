# This is where we test our program

from SyntaxTree import *

sign = Signature()

sign.addPredicateSymbol("brije", 2)

const1 = ConstantTerm('b')
var2 = VariableTerm('x')

#brije(c,x)
atom1 = Atom(sign, "brije", [ const1, var2])

#brije(x,x)
atom2 = Atom(sign, "brije", [ var2, var2])

# ~brije(x,x)
not1 = Not(atom2)

fallX = Forall(var2, atom1)
existsB = Exists(const1, fallX)

iff1 = Iff(existsB, not1)
not2 = Not(iff1)

not2.printMe()
print("")
nnf = not2.NNF()
nnf.printMe()

print("")

nnf = nnf.prenex()

nnf.printMe()

print
print

print("-- NEXT EXAMPLE --")
print

sign = Signature()

sign.addPredicateSymbol("P", 2)

varx = VariableTerm("x")
vary = VariableTerm("y")

atomP = Atom(sign, "P", [ varx, vary ])

existsy1 = Exists( vary, atomP )
forallx1 = Forall( varx, existsy1 )

forallx2 = Forall( varx, atomP)
existsy2 = Exists( vary, forallx2 )

impl = Imp( forallx1, existsy2)
print("Formula:")
impl.printMe()

print

impl = Not(impl)
impl = impl.NNF()
print("NNF:")
impl.printMe()

print

impl = impl.prenex()
print("Prenex:")
impl.printMe()

print