import random
import time

def makerandom(idx: int, treshold: int=6) -> int:
    print(f"Initiated makerandom({idx}).")
    i = random.randint(0,10)
    while i <= treshold:
        print(f"makerandom({idx}) == {i} too low; retying.")
        time.sleep(idx+1)   # modelovanie IO operacie - caka sa tolko kolko je index ulohy
        i = random.randint(0,10)
    print(f"---> Finished makerandom({idx}) == {i}")
    return i

def main():
    for i in range(3):
        makerandom(i, 10-i-1)

if __name__ == "__main__":
    random.seed(444)
    t = time.time()
    main()
    print(f"\nTime elapsed: {time.time()-t}")
