import qgates
import cmatrix as cmat
from timeit import timeit

n = 5
Hn_time = timeit('qgates.Hn(n)', number=1000, globals=globals())
Hn_fast_time = timeit('qgates.Hn_fast(n)', number=1000, globals=globals())

print("Hn: ", Hn_time)
print("Hn_fast: ", Hn_fast_time)

print("Hn_fast is", Hn_fast_time/Hn_time, "times slower than Hn.")