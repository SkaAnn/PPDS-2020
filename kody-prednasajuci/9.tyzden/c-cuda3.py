import numpy
from numba import cuda
import math


@cuda.jit
def my_kernel(io_array):
    x, y = cuda.grid(2)
    x_max, y_max = io_array.shape
    if x < x_max and y < y_max:
        io_array[x, y] *= 2


data = numpy.ones((16, 16))
threadsperblock = (16, 16)
blockspergrid_x = int(math.ceil(data.shape[0] / threadsperblock[0]))
blockspergrid_y = int(math.ceil(data.shape[1] / threadsperblock[1]))
blockspergrid = (blockspergrid_x, blockspergrid_y)
my_kernel[blockspergrid, threadsperblock](data)
print(data)
