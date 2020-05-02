import time

def count():
    print("One")
    # time.sleep je blokujuca operacia
    time.sleep(1)   # pomocou cakania sleep je modelovana nejaka blokujuca IO operacia 
    print("Two")

def main():
    for _ in range(3):
        count()

if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter()
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
