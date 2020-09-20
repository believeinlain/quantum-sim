import qsim
import qgates
import cmatrix as cmat
import math
from random import randint
from fractions import Fraction

# pick a composite number N
N = 15
print("N =", N)

# todo: check if N is prime or a power of a prime

# pick an integer a < N such that a and N do not share nontrivial factors (co-prime)
while True:
    a = randint(2, N-1) 
    # if a is co-prime to N, we're done
    if math.gcd(a, N) == 1:
        break
print("a =", a)

# modular exponentiation function a^x % N
def f_ax_mod_N(a, x, N):
    return ( f_ax_mod_N(a, x-1, N)*a ) % N if x > 0 else 1

# modular exponentiation for fixed a and N
def f(x):
    return f_ax_mod_N(a, x, N)

# output bits must be >= log2(N)
n = math.ceil(math.log2(N))
print(n, "output qubits")

# input bits must be 2n
m = 2*n
print(m, "input qubits")

# create unitary operator for modular exponentiation
Ufmn = qgates.Ufmn(m, n, f)

# initialize quantum state
state = qsim.create_state([0 for _ in range(m+n)])

# hadamard transform the inputs
state = qsim.apply_gate(state, qgates.Hn(m))

# apply unitary operator
state = qsim.apply_gate(state, Ufmn)

# measure outputs
y = qsim.measure_range_standard(state, m, m+n-1)
print("output qubits were measured as:", y)

# now for QFT^-1
state = qsim.apply_gate(state, cmat.adjoint(qgates.QFT(m)))

# measure results
x_binary = qsim.measure_range_standard(state, 0, m-1)
x = qsim.int_from_binary_list(x_binary)
print("input qubits were measured as:", x_binary, "=", x)

# find lambda/r which is x/2^m
lambda_r = Fraction(x, 2**m)
r = lambda_r.denominator
print("r =", r) 
# todo: repeat if r does not divide evenly into 2^m
print("2^m =", 2**m)

# a^r should = 1 Mod N
print("a^r Mod N =", a**r % N)

# todo: if period r is odd, we must choose another a and try again
is_odd = Fraction(r, 2).numerator == r
print("r is", "odd" if is_odd else "even")

# todo: make sure a^r/2 != -1 Mod N, if it is, choose another a and try again
print("a^r/2 =", a**int(r/2))
print("a^r/2 Mod N =", a**int(r/2) % N)
print("-1 Mod N =", -1 % N)

# find a factor of N
factor1 = math.gcd(a**int(r/2) + 1, N)
factor2 = math.gcd(a**int(r/2) - 1, N)
print("two factors of N are", factor1, "and", factor2)

# i think it always returns 1 for some reason lmao