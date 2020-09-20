import cmath
import math
from copy import deepcopy

# matrices to be used with these functions are 2D arrays of numbers
# stored as column arrays of row arrays

# create a matrix full of zeros
def zero_matrix(rows, cols):
    return [ [ 0 for _ in range(cols) ] for _ in range(rows) ]

# create a matrix full of a
def create_matrix(rows, cols, a):
    return [ [ a for _ in range(cols) ] for _ in range(rows) ]

# create an identity matrix of given size
def eye(m, n):
    result = zero_matrix(m, n)
    for i in range(min(m, n)):
        result[i][i] = 1
    return result

# create a column vector from the input array
def column_vector(A):
    n = len(A)
    result = zero_matrix(n, 1)
    for i in range(n):
        result[i][0] = A[i]
    return result

# add two matrices together elementwise
def add(M1, M2):
    # don't alter input arguments
    result = deepcopy(M1)

    # undefined if M1 and M2 are not the same size
    if len(M1) != len(M2) or len(M1[0]) != len(M2[0]):
        print("Elementwise addition undefined if M1 and M2 are not the same size.")
        return result
    
    for i in range(len(M1)):
        for j in range(len(M1[0])):
            result[i][j] += M2[i][j]
    
    return result

# multiply a scalar with a matrix
def scalar_multiple(scalar, M):
    # don't alter input arguments
    result = deepcopy(M)

    for i in range(len(M)):
        for j in range(len(M[0])):
            result[i][j] *= scalar
    
    return result

# sum all elements of a given matrix
def sum(M):
    # M is a matrix with m rows and n columns
    m = len(M)
    n = len(M[0])

    s = 0
    for i in range(m):
        for j in range(n):
            s += M[i][j]
    
    return s

# compute the matrix product of M1 and M2
def product(M1, M2):
    # n is the columns in M1
    n = len(M1[0])
    # M1 has m rows and n columns
    m = len(M1)
    # undefined if columns in M1 != rows in M2
    if (n != len(M2)):
        print("Matrix product undefined if columns of first matrix != rows of second matrix.")
        return 0
    # M2 has n rows and p columns
    p = len(M2[0])
    # result has m rows and p columns
    result = zero_matrix(m, p)

    # fill result with the correct values
    for j in range(m):
        for k in range(p):
            s = 0
            for h in range(n):
                s += M1[j][h] * M2[h][k]
            result[j][k] = s

    return result

# compute the transpose of M
def transpose(M):
    # M is a matrix with m rows and n columns
    m = len(M)
    n = len(M[0])
    # The transpose should have n rows and m columns
    result = zero_matrix(n, m)
    # fill the empty result matrix with the transposed values
    for i in range(m):
        for j in range(n):
            result[j][i] = M[i][j]
    return result

# find the complex conjugate transpose of matrix M
def adjoint(M):
    # first find the transpose
    result = transpose(M)
    # then find the complex conjugate of each element
    for i in range(len(result)):
        for j in range(len(result[0])):
            result[i][j] = result[i][j].conjugate()
    return result

# calculate the trace as the sum of diagonal elements
def trace(M):
    # undefined if matrix is not square
    if (len(M) != len(M[0])):
        print("Trace undefined if matrix is not square.")
        return 0
    
    s = 0
    # M has dimensions n x n
    n = len(M)
    for i in range(n):
        s += M[i][i]

    return s

# calculate the inner product of two matrices (frobenius style)
def inner(M1, M2):
    return trace(product(adjoint(M1), M2))

# calculate the norm of a matrix (frobenius style)
def norm(M):
    # use the real part since the imaginary part must be zero
    return math.sqrt(inner(M, M).real)

# determine if two matrices are equal
def is_equal(M1, M2):
    # are they the same size?
    if len(M1) != len(M2) or len(M1[0]) != len(M2[0]):
        return False
    
    # check if all elements are equal
    for i in range(len(M1)):
        for j in range(len(M1[0])):
            # if any element is not equal, we're done
            if not cmath.isclose(M1[i][j], M2[i][j]):
                return False

    return True

# determine if a matrix is hermitian
def is_hermitian(M):
    # M is hermitian iff it equals its conjugate transpose
    return is_equal(adjoint(M), M)

# calculate the expected value of operator O on state V
def expected_value(O, V):
    value = inner(product(O, V), V)
    # if O is hermitian, the expected value will be real
    if is_hermitian(O):
        return value.real
    else:
        return value 

# determine the commutator of two operators
def commutator(O1, O2):
    # should return 0 matrix if commutative
    return add(product(O1, O2), scalar_multiple(-1, product(O2, O1)))

# "demean" the given operator for a given state
def demean(O, V):
    # subtract the expected value along the diagonal of O
    return add(O, scalar_multiple(-1*expected_value(O, V), eye(len(O), len(O[0]) )))

# calculate the variance
def variance(O, V):
    return expected_value(product(demean(O, V), demean(O, V)), V)

# calculate the tensor product between two matrices
def tensor_product(M1, M2):
    # m is number of rows, n is number of columns
    m1 = len(M1)
    n1 = len(M1[0])
    m2 = len(M2)
    n2 = len(M2[0])
    # result will have m1*m2 rows and n1*n2 columns
    result = zero_matrix(m1*m2, n1*n2)
    # iterate through each element of M1
    for i1 in range(m1):
        for j1 in range(n1):
            # iterate through each element of M2
            for i2 in range(m2):
                for j2 in range(n2):
                    # multiply each element in M1 with a copy of M2 basically
                    result[m2*i1+i2][n2*j1+j2] = M1[i1][j1] * M2[i2][j2]

    return result

