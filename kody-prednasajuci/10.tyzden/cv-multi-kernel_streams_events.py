from numba import cuda
import numpy as np
from time import perf_counter


NUM_ARRAYS = 200
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


data = []
data_gpu = []
gpu_out = []
streams = []
start_events = []
end_events = []

for _ in range(NUM_ARRAYS):
    streams.append(cuda.stream())
    start_events.append(cuda.event())
    end_events.append(cuda.event())
    data.append(np.random.randn(ARRAY_LEN).astype('float32'))

t_start = perf_counter()

for k in range(NUM_ARRAYS):
    data_gpu.append(cuda.to_device(data[k], stream=streams[k]))

for k in range(NUM_ARRAYS):
    start_events[k].record(stream=streams[k])
    kernel[1, 64, streams[k]](data_gpu[k])

for k in range(NUM_ARRAYS):
    end_events[k].record(stream=streams[k])

for k in range(NUM_ARRAYS):
    gpu_out.append(data_gpu[k].copy_to_host(stream=streams[k]))

t_end = perf_counter()

for k in range(NUM_ARRAYS):
    assert(np.allclose(gpu_out[k], data[k]))

kernel_times = []
for k in range(NUM_ARRAYS):
    kernel_times.append(cuda.event_elapsed_time(start_events[k], end_events[k]))

print(f'Total time: {t_end - t_start}')
print(f'Mean kernel duration (milliseconds): {np.mean(kernel_times)}')
print(f'Mean kernel standard deviation (milliseconds): {np.std(kernel_times)}')
