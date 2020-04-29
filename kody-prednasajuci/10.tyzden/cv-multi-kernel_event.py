from numba import cuda
import numpy as np
from time import perf_counter


ARRAY_LEN = 1024**2


@cuda.jit
def kernel(array):
    thd = cuda.grid(1)
    num_iters = array.size / cuda.blockDim.x
    for j in range(num_iters):
        i = j * cuda.blockDim.x + thd
        for k in range(50):
            array[i] *= 2
            array[i] /= 2


data = np.random.randn(ARRAY_LEN).astype('float32')
data_gpu = cuda.to_device(data)

start_event = cuda.event()
end_event = cuda.event()

start_event.record()
kernel[1, 64](data_gpu)
end_event.record()

end_event.synchronize()

print(f'Has the kernel started yet? {start_event.query()}')
print(f'Has the kernel ended yet? {end_event.query()}')


print(f'Kernel execution time in milliseconds: {cuda.event_elapsed_time(start_event, end_event)}')


# print(f'Total time: {}')
