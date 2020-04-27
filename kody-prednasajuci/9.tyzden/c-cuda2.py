import numpy
from numba import cuda


@cuda.jit
def my_kernel(io_array):
    pos = cuda.grid(1)
    if pos < io_array.size:
        io_array[pos] *= 2


data = numpy.ones(256)
threadsperblock = 32
blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock
my_kernel[blockspergrid, threadsperblock](data)
print(data)
