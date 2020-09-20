import qsim
import qgates
from random import randint
from math import sqrt

# number of bits on which f operates
n = 6

# secret element for which f(x) = 1 iff x = c
c = randint(0, 2**n-1)
print("Secret:", c)

# define f(x) = 1 iff x = c
def f(x):
    return 1 if x == c else 0

# create unitary operator for f such that x -> x and y -> y XOR f(x)
Uf = qgates.Uf(n, f)

# create hadamard operator for n qubits
Hn = qgates.Hn(n)

# create mean inversion operator for n qubits
MI = qgates.mean_inversion(n)

# initialize quantum state
state = qsim.create_state([0 for _ in range(n)] + [1])

# apply hadamard to x
state = qsim.apply_gate(state, Hn)

# apply hadamard to y
state = qsim.apply_gate(state, qgates.H, n)

# number of times to repeat
loop = int(sqrt(2**n))

# repeat sqrt(2**n) times
for i in range(loop):
    # apply Uf to x
    state = qsim.apply_gate(state, Uf)

    # apply mean inversion to x
    state = qsim.apply_gate(state, MI)

# get results
result = qsim.measure_all_standard(state)

# print x values
print("Guess:", qsim.int_from_binary_list([result[i] for i in range(n)]))