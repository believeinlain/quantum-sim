import qsim
import qgates
from cmatrix import is_equal
from random import shuffle
from random import randint
from random import seed
from math import log2
from copy import deepcopy

#seed(1)

# number of bits on which f operates
n = 3
size = 2**n

# secret binary number for which f(x) = f(y) iff x_i = y_i XOR c_i
c = randint(0, size)

# print secret number
print("secret c =", c)

# create a list of pairs that must match
f_pairs = set()
for i in range(size):
    # match a pair so that x_i = y_i XOR c_i
    pair = [i, i^c]
    # sort the pair so that only unique pairs are added
    pair.sort()
    # add pair as tuple so it is hashable
    f_pairs.add( tuple(pair) )

# create a list of all possible outputs of f
f_outputs = [i for i in range(size)]
# randomize the list to create an arbitrary function that
# fits the given requirements
shuffle(f_outputs)

# map outputs to pair values
f_map = {}
for p in f_pairs:
    # get a new shared output for each pair
    shared_output = f_outputs.pop()
    for e in p:
        # map each element in the pair to the shared output
        f_map[e] = shared_output

# map the remaining possible outputs to different unused values
for i in range(size):
    if not i in f_map and len(f_outputs)>0:
        f_map[i] = f_outputs.pop()

# define f as a function that produces the appropriate output
# so that f(x) = f(y) iff x_i = y_i XOR c_i
def f(x):
    return f_map[x]

# create a unitary operator for f such that x -> x and y -> y XOR f(x)
Ufn = qgates.Ufn(n, f)

# empty set of results
results = set()
# keep track of how many times we had to run the algorithm
runs = 0

# run quantum algorithm until we have n different results
while len(results) < n:
    runs += 1
    # initialize |x,y> as |0,0>
    state = qsim.create_state(qsim.get_binary_list(0, n*2))

    # apply hadamard to |x>
    state = qsim.apply_gate(state, qgates.Hn(n), 0)

    # apply Ufn 
    state = qsim.apply_gate(state, Ufn, 0)

    # apply hadamard to |x>
    state = qsim.apply_gate(state, qgates.Hn(n), 0)

    # measure
    result = qsim.measure_all_standard(state)
    # add the measured x value to our set of results
    results.add(qsim.int_from_binary_list([result[i] for i in range(0, n)]))

print("Ran quantum algorithm", runs,"times.")

# the set of results are all numbers for which the inner product of them with c = 0
equations = list(results)

# remove all zero equations from list
equations[:] = [eq for eq in equations if eq != 0]

# cycle through place from MSB to LSB
for i in reversed(range(n)):
    # keep list of indices of results to add
    to_add = []
    for c in range(len(equations)):
        # if c has a 1 in place i, keep track of it
        if equations[c]&(2**i): 
            to_add.append(c)
        # if we have two or more numbers to add
        if len(to_add) > 1:
            # "add" the first to each successive member
            for j in range(1, len(to_add)):
                equations[to_add[j]] = equations[to_add[j]]^equations[to_add[0]]

# start guess with all ones
c_known = 2**n - 1

# if an equation has only one bit = 1 then the bit in c must be 0
for eq in equations:
    if log2(eq).is_integer():
        c_known = c_known^eq

# remove all single bit equations
equations[:] = [eq for eq in equations if not log2(eq).is_integer()]

# if we're lucky we already found c by now
if len(equations) == 0:
    print("Found c =", c_known)

# for each equation with exactly two bits anywhere, those two bits must match
# so the total number of guesses needed goes down by half for each of those

# for each equation with exactly three bits anywhere, two of those bits must be 1
# or all zero