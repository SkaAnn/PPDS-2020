from __future__ import division
from numba import cuda
import numpy
import math
 
 
@cuda.jit
def my_kernel_2D(io_array):
    x, y = cuda.grid(2)
    ### YOUR SOLUTION HERE
    # namiesto io_array.size pouzite io_array.shape
    if x < io_array.shape[0] and y < io_array.shape[1]:
         io_array[x][y] *= 2
 
# praca s 2rozmernym polom na vstupe
data = numpy.ones((16, 16)) # (16, 70)
threadsperblock = (16, 16)  # (16, 32)
blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
print(blockspergrid_x)
blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
print(blockspergrid_y)
blockspergrid = (blockspergrid_x, blockspergrid_y)
print(blockspergrid)
my_kernel_2D[blockspergrid, threadsperblock](data)
print(data)
