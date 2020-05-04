import numpy
from numba import cuda
print(cuda.gpus)

# kernel funkcia = funkcia vyvolana na CPU (hostovi) ale bezi na GPU (device)
# 1. nesmie vracat ziadnu hodnotu! vysledky nutne odovzdavat pomocou pola na vstupe fun
# 2. pri spusteni sa definuje struktura vypoctovych vlakien
#   - pocet vlaken v bloku
#   - pocet blokov

# DEFINICIA KERNELU
@cuda.jit
def my_kernel(io_array):
    # VYPOCET INDEXU DO POLA PRE VLAKNO
    # Thread id in a 1D block
    tx = cuda.threadIdx.x   # pozicia vlakna v bloku
    # Block id in a 1D grid
    ty = cuda.blockIdx.x    # pozicia bloku v gride
    # Block width, i.e. number of threads per block
    bw = cuda.blockDim.x   # pocet vlaken v bloku
    # Compute index inside the array
    pos = tx + ty * bw
    # ALEBO VYSSIE UVEDENE 4 RIADKY NAHRAD pos = cuda.grid(1)
    
    # Check array boundaries
    if pos < io_array.size: # treba kontrolovat! Lebo mozme pristupovat k udajom mimo pola
        # do the computation
        io_array[pos] *= 2

# najdolezitejsie zvolit vhodne parametre vypoctu - pocet blokov, pocet vlaken
# celkovy pocet vlaken = pocet blokov * pocet vlaken v bloku

# Create the data array - usually initialized some other way
data = numpy.ones(256)
 
# Set the number of threads in a block
# pocet vlaken v bloku by mal byt vzdy nasobok warpu (32 vlaken)
# vsetky vlakna vo warpe vykonavaju ten isty programovy kod
threadsperblock = 32 
 
# Calculate the number of thread blocks in the grid
# pocet blokov v gride
blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock
print(blockspergrid)

# Now start the kernel
my_kernel[blockspergrid, threadsperblock](data)

# Print the result
print(data)
