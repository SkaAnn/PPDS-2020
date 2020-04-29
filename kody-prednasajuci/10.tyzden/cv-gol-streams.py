from numba import cuda
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


@cuda.jit(device=True)
def nbrs(x, y, matrix):
    return (matrix[x - 1, y + 1] + matrix[x - 1, y] + matrix[x - 1, y - 1] +
            matrix[x, y + 1] + matrix[x, y - 1] + matrix[x + 1, y - 1] +
            matrix[x + 1, y] + matrix[x + 1, y + 1])


@cuda.jit
def kernel(lattice_out, lattice):
    x, y = cuda.grid(2)
    n = nbrs(x, y, lattice)

    if lattice[x, y] == 1:
        if n in (2, 3):
            lattice_out[x, y] = 1
        else:
            lattice_out[x, y] = 0
    elif lattice[x, y] == 0:
        if n == 3:
            lattice_out[x, y] = 1
        else:
            lattice_out[x, y] = 0


def update_gpu(frame_num, imgs, new_lattices_gpu, lattices_gpu, N, streams,
               num_concurrent):
    blockdim = (N // 32, N // 32)
    griddim = (32, 32)
    for k in range(num_concurrent):
        kernel[griddim, blockdim, streams[k]](new_lattices_gpu[k],
                                              lattices_gpu[k])

        imgs[k].set_data(new_lattices_gpu[k].copy_to_host(stream=streams[k]))

        lattices_gpu[k].copy_to_device(new_lattices_gpu[k], stream=streams[k])

    return imgs


N = 128
NUM_CONCURRENT = 4

streams = []
lattices_gpu = []
new_lattices_gpu = []

for k in range(NUM_CONCURRENT):
    streams.append(cuda.stream())
    lattice = np.int32(
        np.random.choice([1, 0], N * N, p=[0.25, 0.75]).reshape(N, N)
    )
    lattices_gpu.append(cuda.to_device(lattice))

    new_lattice_gpu = cuda.device_array_like(lattices_gpu[k])
    new_lattices_gpu.append(new_lattice_gpu)

fig, ax = plt.subplots(nrows=1, ncols=NUM_CONCURRENT)
imgs = []

for k in range(NUM_CONCURRENT):
    imgs.append(ax[k].imshow(lattices_gpu[k].copy_to_host(stream=streams[k]),
                             interpolation='nearest'))



ani = animation.FuncAnimation(fig,
                              update_gpu,
                              fargs=(
                                  imgs,
                                  new_lattices_gpu,
                                  lattices_gpu,
                                  N,
                                  streams,
                                  NUM_CONCURRENT
                              ),
                              interval=33,
                              frames=1000)
plt.show()
