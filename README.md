#Gilmore's algorithm

Gilmore's algorithm is based on a fact that the problem of satisfiability of formulas in
first order is semi-decidable, if a formula is unsatisfiable there is a decision procedure that will prove it's unsatisfiability.

If *S(i)* is the set of ground clauses obtained by replacing the variables in formula *S* with the constants in the i-th level constant
set of the [Herbrand Universe](http://mathworld.wolfram.com/HerbrandUniverse.html), then all of the elements of *S(i)* must be satisfiable in order for the starting formula *S* to be satisfiable.

Gilmore's algorithm uses the multiplication method to find an unsatisfiable element of *S(i)*. It is not guarateed that the algorithm will find the proof.
