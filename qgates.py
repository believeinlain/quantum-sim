import cmatrix as cmat
import qsim
from math import sqrt, cos, sin, pi
from cmath import exp
from copy import deepcopy

# bits
one = [[0], 
       [1]]
zero = [[1], 
        [0]]

# pauli operators
Sx = [[0, 1], 
      [1, 0]]
Sy = [[0, -1j], 
      [1j, 0]]
Sz = [[1, 0], 
      [0, -1]]

# S gate
S = [[1, 0],
     [0, 1j]]

# T gate
T = [[1, 0],
     [0, 1/sqrt(2)+1j/sqrt(2)]]

# square root of NOT gate
sqrtnot = [[1/sqrt(2), -1/sqrt(2)],
           [1/sqrt(2), 1/sqrt(2)]]

# hadamard gate
# basically rotates pi about Z-axis then pi/2 about Y-axis on bloch sphere
# analagous to 1-qubit fourier transform
H = [[1/sqrt(2), 1/sqrt(2)],
     [1/sqrt(2), -1/sqrt(2)]]

# acts on |x>, returns |!x>
qnot = [[0, 1],
        [1, 0]]

# acts on |xy>, returns |x, x XOR y>
# basically inverts y iff x is 1
cnot = [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]]

# acts on |xyz>, returns |xy, z XOR (x && y)>
# basically inverts z iff x and y are both 1
toffoli = [[1, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 0, 1, 0]]

# acts on |xyz>, returns |x, y XOR s, z XOR s>, where s = (y XOR z) && x
# basically swaps y and z iff x is 1
fredkin = [[1, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 1]]

# phase shift gate (longitude change)
def R(theta):
      return [[1, 0],
              [0, exp(theta)]]

# rotate around x-axis
def Rx(theta):
      return [[cos(theta/2), -1j*sin(theta/2)],
              [-1j*sin(theta/2), cos(theta/2)]]

# rotate around y-axis
def Ry(theta):
      return [[cos(theta/2), -sin(theta/2)],
              [sin(theta/2), cos(theta/2)]]

# rotate around z-axis
def Rz(theta):
      return [[exp(-1j*theta/2), 0],
              [0, exp(1j*theta/2)]]

# conditional unitary gate, where U is any unitary gate on 1 qubit
def CU(U):
      return [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, U[0][0], U[0][1]],
              [0, 0, U[1][0], U[1][1]]]

# Deutsch gate (conditional rotation)
def D(theta):
      return [[1, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, exp(theta)]]

# Hadamard gate for n qubits simultaneously
def Hn(n):
      # start tensor product from first index
      transform = deepcopy(H)

      for _ in range(1, n):
            # tensor product H with itself n times
            transform = cmat.tensor_product(transform, deepcopy(H))
      
      return transform

# construct unitary operator on f(x) for n-bit x and single bit y
# where x-> x and y-> y XOR f(x)
# hard to explain what is going on here
# think of this as the tensor product between the matrix
# [[f(00), 0, 0, 0],
#  [0, f(01), 0, 0],
#  [0, 0, f(10), 0],
#  [0, 0, 0, f(11)]]
# (generalized to n bits) and the matrix
# [[NOT, 1],
#  [1, NOT]]
# where multiplying f(x) by not yields ( not f(x) )
# this works I promise
# Uf will perform x-> x and y-> y XOR f(x)
def Uf(n, f):
      # number of possible x values
      x_perm = 2**n 
      # create empty matrix of appropriate size
      result = cmat.zero_matrix(x_perm*2, x_perm*2)
      for i in range(x_perm):
            for j in range(2):
                  for k in range(2):
                        result[2*i+j][2*i+k] = int(not f(i)) if j==k else f(i)
      
      return result

# create a unitary operator for any f from {0, 1}^n -> {0, 1}^n
# for n-bit x and x-bit y, of course x -> x and y -> y XOR f(x)
# it works I can't believe it was this easy
def Ufn(n, f):
      # number of possible x or y values
      perm = 2**n 
      # create empty matrix of appropriate size
      result = cmat.zero_matrix(perm**2, perm**2)
      
      # iterate through all possible x values
      for x in range(perm):
            # find f(x)
            f_x = f(x)
            # iterate through possible y values
            for y in range(perm):
                  # find y XOR f(x)
                  xor = y^f_x
                  # for each row in this block, set 1 iff xor == row number
                  for row in range(perm):
                        result[x*perm+row][x*perm+y] = 1 if xor==row else 0
      
      return result

# create a unitary operator for any f from {0, 1}^m -> {0, 1}^n
# for m-bit x and x-bit y, of course x -> x and y -> y XOR f(x)
def Ufmn(m, n, f):
      # number of possible x values
      x_perm = 2**m 
      # number of possible y values
      y_perm = 2**n 
      # create empty matrix of appropriate size
      result = cmat.zero_matrix(x_perm*y_perm, x_perm*y_perm)
      
      # iterate through all possible x values
      for x in range(x_perm):
            # find f(x)
            f_x = f(x)
            # iterate through possible y values
            for y in range(y_perm):
                  # find y XOR f(x)
                  xor = y^f_x
                  # for each row in this block, set 1 iff xor == row number
                  for row in range(y_perm):
                        result[x+row][x+y] = 1 if xor==row else 0
      
      return result

# create a unitary operator that performs an inversion about the mean on n qubits
def mean_inversion(n):
      # number of possible x or y values
      perm = 2**n 
      # create average matrix of appropriate size
      A = cmat.create_matrix(perm, perm, 1/perm)

      return cmat.add(cmat.scalar_multiple(-1, cmat.eye(perm, perm)), A)

# create a list of the n complex roots of unity (1+0i)
def unity_roots(n):
      return [exp(2*pi*1j*k/n) for k in range(n)]

# create a vandermonde matrix (matrix that evaluates a polynomial described by
# a column vector of coefficients for each x in x_list)
def vandermonde(n, x_list):
      return [[x_n**i for i in range(n)] for x_n in x_list]

# get a quantum fourier transform matrix
def QFT(n):
      return cmat.scalar_multiple(1/sqrt(2**n), vandermonde(2**n, unity_roots(2**n)))
