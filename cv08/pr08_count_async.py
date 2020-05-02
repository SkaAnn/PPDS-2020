import time
import asyncio

# moze konkurentne vykonavat kod
async def count():
    print("One")
    # nemozme volat funkciu ktora je blokujuca, tak pouzi neblokujuci sleep z asyncio
    await asyncio.sleep(1)  # musim cakat ale chod robit nieco uzitocne - povie sa slucke udalosti
    # stopne sa pred tymto volanim a zacne sa vykonavat dalsi task
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

async def noop():
    pass

if __name__ == "__main__":
    s = time.perf_counter()
    # print(noop())    # nie je mozne priamo volat korutinu
    asyncio.run(main())
    elapsed = time.perf_counter()
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
