import numpy as np
from simplex_integer import simplex_integer
from fractions import Fraction
# np.set_printoptions(suppress=True, formatter={'all':lambda x: str(Fraction(x).limit_denominator())})

s = simplex_integer('input/in_1.txt', True)
s.printSolution()