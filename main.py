# This is where we test our program

from syntax_tree import *

sign = Signature()

sign.add_predicate_symbol("brije", 2)

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

not2.print_me()
print("")
nnf = not2.nnf()
nnf.print_me()

print("")

nnf = nnf.prenex()

nnf.print_me()

print
print

print("-- NEXT EXAMPLE --")
print

sign = Signature()

sign.add_predicate_symbol("P", 2)

varx = VariableTerm("x")
vary = VariableTerm("y")

atomP = Atom(sign, "P", [ varx, vary ])

existsy1 = Exists( vary, atomP )
forallx1 = Forall( varx, existsy1 )

forallx2 = Forall( varx, atomP)
existsy2 = Exists( vary, forallx2 )

impl = Imp( forallx1, existsy2)
impl = Not(impl)
print("Formula:")
impl.print_me()

print

impl = impl.nnf()
print("NNF:")
impl.print_me()

print

impl = impl.prenex()
print("Prenex:")
impl.print_me()

print