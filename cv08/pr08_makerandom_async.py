import random
import time
import asyncio

async def makerandom(idx: int, treshold: int=6) -> int:
    print(f"Initiated makerandom({idx}).")
    i = random.randint(0,10)
    while i <= treshold:
        print(f"makerandom({idx}) == {i} too low; retying.")
        # MUSIME ODSTRANIT AJ BLOKUJUCE VOLANIA
        # time.sleep(idx+1)   # modelovanie IO operacie - caka sa tolko kolko je index ulohy
        await asyncio.sleep(idx+1)
        i = random.randint(0,10)
    print(f"---> Finished makerandom({idx}) == {i}")
    return i

async def main():   # asynchronna funkia
    # MUSIME TO AJ SPUSTAT ASYNCHRONNE
    # * kvoli rozbitiu zoznamu na polozky
    await asyncio.gather(* (makerandom(i, 10-i-1) for i in range(3)))  # asynchronne volanie funkcii

if __name__ == "__main__":
    random.seed(444)
    t = time.time()
    asyncio.run(main()) # slucka udalosti
    # trva to tak dlho ako trva beh najpomalsej z funkcii
    print(f"\nTime elapsed: {time.time()-t}")
