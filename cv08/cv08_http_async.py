# asynchronne HTTP poziadavky - externy modul aiohttp
import asyncio
import aiohttp
import time
 
# korutina (vdaka async)
async def task(name, work_queue):
    # session vramci ktorej sa budeme pripajat
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"Task {name} getting URL: {url}")
            time_start = time.perf_counter()
            # async with umoznuje vykonavanie korutiny pri vstupe a vystupe z with bloku 
            async with session.get(url) as response:
                await response.text()   # precitanie tela odpovede
            elapsed = time.perf_counter() - time_start
            print(f"Task {name} elapsed time: {elapsed:.1f}")
 
 
async def main():
    # Create the queue of work
    work_queue = asyncio.Queue()
 
    # Put some work in the queue
    for url in [
            "http://google.com",
            "http://stuba.sk",
            "http://linkedin.com",
            "http://apple.com",
            "http://microsoft.com",
            "http://facebook.com",
            "http://twitter.com",
    ]:
        await work_queue.put(url)
 
    # Run the tasks
    start_time = time.perf_counter()
    # manazovanie korutin
    await asyncio.gather(
        task("One", work_queue),
        task("Two", work_queue),
    )
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")
 
 
if __name__ == "__main__":
    asyncio.run(main())
