import numpy
from numba import cuda


@cuda.jit
def my_kernel(io_array):
    tx = cuda.threadIdx.x
    ty = cuda.blockIdx.x
    bw = cuda.blockDim.x

    pos = bw * ty + tx

    if pos < io_array.size:
        io_array[pos] *= 2


data = numpy.ones(256)
threadsperblock = 32
blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock
my_kernel[blockspergrid, threadsperblock](data)
print(data)
