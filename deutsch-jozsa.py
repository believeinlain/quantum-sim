import qsim
import qgates
import cmatrix as cmat
from random import randint
from random import shuffle

# number of bits on which f operates
n = 5

# number of qubits we need
m = n+1

# name indices
x = [i for i in range(n)]; y = n

# code determining f is here so that f does not change each call

# f will be either completely balanced or constant
f_is_balanced = bool(randint(0, 1))
# if f is constant, it will always return the same value
f_constant = randint(0, 1)
# if f is balanced, it will return the value f_balanced[x]
# this value must be 1 exactly half of the time
x_perm = 2**n # number of possible x values
# fill the first half of f_balanced with 1
f_balanced = [(1 if i < x_perm/2 else 0) for i in range(x_perm)]
# then shuffle to get a random balanced function
shuffle(f_balanced)

# f takes an integer and returns 1 or 0
def f(x):
    if (f_is_balanced):
        return f_balanced[x]
    else:
        return f_constant

# construct unitary matrix such that x-> x and y-> y XOR f(x)
Uf = qgates.Uf(n, f)

# initialize qubits
state = qsim.create_state([0 for _ in range(n)] + [1]) # x = |0...0>, y = |1>

# place all x in superpostion of all permutations of x
state = qsim.apply_gate(state, qgates.Hn(n), 0)

# place y in superposition of |0> - |1>
state = qsim.apply_gate(state, qgates.H, y)
# sidenote: this is equivalent to one H^n of all qubits
# doing it this way is slower less but easier to explain?

# apply Uf
state = qsim.apply_gate(state, Uf, 0)

# return x to a deterministic state
state = qsim.apply_gate(state, qgates.Hn(n), 0)

# measure qubits
result = qsim.measure_all_standard(state)

# print result
print("f was", "balanced" if f_is_balanced else ("constant 1" if f_constant==1 else "constant 0") )
print("x =", [result[i] for i in x])

# if x is all 0, then f is constant, else f is balanced