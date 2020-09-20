import qsim
import qgates
from random import randint

# the four possible functions from {0, 1} -> {0, 1}
f_one = [[0, 0],
         [1, 1]]
f_same = [[1, 0],
          [0, 1]]
f_swap = [[0, 1],
          [1, 0]]
f_zero = [[1, 1],
          [0, 0]]

# unitary operators from f (x->x, y-> y XOR f(x) )

# always flips y, regardless of x
Uf_one = [[0, 1, 0, 0],
          [1, 0, 0, 0],
          [0, 0, 0, 1],
          [0, 0, 1, 0]]
# only flips y if x is 1
Uf_same = [[1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 0, 1],
           [0, 0, 1, 0]]
# only flips y if x is 0
Uf_swap = [[0, 1, 0, 0],
           [1, 0, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1]]
# never flips y, regardless of x
Uf_zero = [[1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1]]

# pick a random unitary operator
Uf_list = [Uf_one, Uf_same, Uf_swap, Uf_zero]
Uf_tattle = ["one", "same", "swap", "zero"]
Uf_balance = ["constant", "balanced", "balanced", "constant"]
Uf_select = randint(0, 3)
Uf = Uf_list[Uf_select]

# define variables to be used as indices in the combined state
x = 0; y = 1

# initialize 2 qubits at |01>
state = qsim.create_state([0, 1])

# apply hadamard to x
state = qsim.apply_gate(state, qgates.H, x)

# apply hadamard to y
state = qsim.apply_gate(state, qgates.H, y)

# apply our random operator
state = qsim.apply_gate(state, Uf, 0)

# apply hadamard to x to reach deterministic state
state = qsim.apply_gate(state, qgates.H, x)

# measure qubits
result = qsim.measure_all_standard(state)

# print result
print("x =", result[x])
# which operator was it?
print("Uf was", Uf_balance[Uf_select])