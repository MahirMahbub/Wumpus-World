from typing import List, Dict
from sympy import *
from sympy.logic.boolalg import to_cnf
from sympy.abc import A, B, D
from sympy.logic.inference import satisfiable
from sympy import Symbol
from sympy.logic import simplify_logic
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
cnf_1 = simplify_logic(to_cnf(x>> ~y|z))
cnf_2 = simplify_logic(to_cnf(~(x | y) >> z))
print(satisfiable(cnf_1 & cnf_2))