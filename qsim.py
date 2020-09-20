import cmatrix as cmat
import qgates
from random import random
from copy import deepcopy
from math import log
from math import sqrt

# define standard basis (for measuring)
P0 = [[1, 0],
      [0, 0]]
P1 = [[0, 0],
      [0, 1]]

# probability that qubit Q will be measured as a one in the standard basis
def probability_one(Q):
    return cmat.expected_value(P1, Q)

# measure qubit Q in the standard basis
def measure_standard(Q):
    p1 = probability_one(Q)
    # pick a number between 0 and 1
    r = random()
    # if r < p1, we rolled a 1, otherwise we rolled a zero
    if (r < p1):
        # collapse the qubit
        Q[0] = deepcopy(qgates.one[0])
        Q[1] = deepcopy(qgates.one[1])
        return 1
    else:
        # collapse the qubit
        Q[0] = deepcopy(qgates.zero[0])
        Q[1] = deepcopy(qgates.zero[1])
        return 0

# convert i to a binary list of n bits
def get_binary_list(i, n):
    # first create an empty list n bits long
    binary = [ 0 for _ in range(n) ]
    # then find each bit
    r = i
    # iterate through each bit
    for b in reversed(range(n)):
        # find the place value of b
        power = 2**b
        # set the bit to 1 if power fits in r
        binary[b] = 1 if (power <= r) else 0
        # if 1, subtract power from r
        if binary[b]: r -= power
    
    # following the above algorithm returns the MSB last
    binary.reverse()
    return binary

# convert a binary list to an integer
def int_from_binary_list(b_list):
    sum = 0
    b = deepcopy(b_list)
    b.reverse()
    for i in range(len(b)):
        if b[i]: sum += 2**i
    return int(sum)

# choose a random number from a list of probabilities
# returns the index in prob_list of the chosen number
def choose_from(prob_list):
    #print("prob_list: ", prob_list)
    # create a sum list where each element is + the sum of all
    # preceding elements in prob_list
    sum_list = []
    for i in range(len(prob_list)):
        sum = 0
        for j in range(i+1):
            sum += prob_list[j]
        sum_list.append(sum)

    # random number between 0 and 1
    r = random()
    
    # the last element of sum_list should really be 1, but lets scale anyway
    r *= sum_list[len(sum_list)-1]

    # return the index just before the point at which r passed the sum
    for k in range(len(sum_list)):
        if r <= sum_list[k]:
            return k
    
    # should never get here
    return 0

# create a qubit initialized at b
def create_qubit(b):
    return deepcopy(qgates.one if b else qgates.zero)

# create a combined state with len(b) qubits all at b_list[i]
# 6 qubits and things start getting really slow
def create_state(b_list):
    state = create_qubit(b_list[0])

    for i in range(1, len(b_list)):
        # keep performing tensor products with new qubits
        state = cmat.tensor_product(state, create_qubit(b_list[i]))
    
    return state

# get the number of bits in a combined state
def get_num_bits(state):
    # there should be 2^n rows and cols in state
    n = log(len(state), 2)
    # if n isn't a whole number we have a problem
    if not (n).is_integer():
        print("Unable to determine number of qubits from combined state.")
        return 0
    
    return int(n)

# apply the given m-qubit gate to the given state starting at index
def apply_gate(state, gate, index=0):
    n = get_num_bits(state)
    m = get_num_bits(gate)
    if m>n:
        print("Cannot apply ", m, "-qubit gate on ", n," qubits.")
        return state

    # start tensor product from first index
    transform = deepcopy(gate) if index==0 else cmat.eye(2,2)

    for j in range(1, n):
        # apply gate at index
        if j == index:
            transform = cmat.tensor_product(transform, deepcopy(gate))
        # skip over m qubits after index
        elif index < j and j < index+m:
            continue
        # otherwise tensor product an identity gate
        else:
            transform = cmat.tensor_product(transform, cmat.eye(2,2))

    # return the transformed state
    return cmat.product(transform, state)

# get the projector matrix on n qubits for state i
# for a given i the projector will be an n-bit tensor product of P0 and P1
def get_projector(i, n):
    # convert i to n bit binary
    binary = get_binary_list(i, n)

    # start tensor product from MSB
    projector = deepcopy(P1) if binary[0]==1 else deepcopy(P0)

    for j in range(n-1):
        # keep performing tensor products with the appropriate basis
        projector = cmat.tensor_product(projector, deepcopy(P1) if binary[j+1]==1 else deepcopy(P0))
    
    # store the expected value of each permutation in probabilities
    return projector

# get the projector matrix from qubits a to b for state i
# for a given i the projector will be an n-bit tensor product of P0 and P1 from a to b
# padded with identity on both sides
def get_projector_range(i, a, b, n):
    # if a is 0 just get the projector up to b
    if a == 0:
        total = get_projector(i, b+1)
    # otherwise start the total from identity up to a then the projector up to b
    else:
        total = cmat.eye(2**a, 2**a)
        total = cmat.tensor_product(total, get_projector(i, b-a+1))

    # finally append identity up to n
    for _ in range(b, n-1):
        total = cmat.tensor_product(total, cmat.eye(2, 2))
    
    return total

# collapse the state to the results of measuring qubits a through b in state i of n qubits
def collapse_state(state, i, a, b):
    n = get_num_bits(state)
     
    # apply the total projector to the state
    return cmat.product(get_projector_range(i, a, b, n), state)

# measure a combined state of n qubits on the standard basis
# WARNING: measuring a state necessarily modifies it, since this
# is a quantum computer simulation
def measure_all_standard(state):
    return measure_range_standard(state, 0, get_num_bits(state)-1)

# measure qubits a through b in a combined state of n qubits on the standard basis
# WARNING: measuring a state necessarily modifies it, since this
# is a quantum computer simulation
def measure_range_standard(state, a, b):
    n = get_num_bits(state)
    # length of selected range
    m = b-a+1
    
    # for each permutation, how likely is it?
    probabilities = []
    # each row of state corresponds to a binary output of n bits
    # for each output the operator will be a tensor product of P0 and P1
    # then we just calculate the expected value for each permutation on state
    for i in range(2**m):
        # store the expected value of each permutation in probabilities
        probabilities.append(cmat.expected_value(get_projector_range(i, a, b, n), state))

    # get the list of binary results for each qubit in state
    value = choose_from(probabilities)
    results = get_binary_list(value, m)

    # collapse the state to the tensor product of measured qubits
    # copy the results of collapse_state into state so that it is modified
    # to simulate an actual quantum measurement
    measured_state = cmat.scalar_multiple(1/sqrt(probabilities[value]), collapse_state(state, value, a, b))
    for i in range(len(state)):
        state[i] = measured_state[i]

    return results