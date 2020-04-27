import asyncio
import aiohttp
import time


async def task(name, work_queue):
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f'Task {name} getting url: {url}')
            time_start = time.perf_counter()
            async with session.get(url) as response:
                await response.text()
            elapsed = time.perf_counter() - time_start
            print(f'Task {name} elapsed time: {elapsed:.1f}')


async def main():
    work_queue = asyncio.Queue()

    for url in [
            'http://google.com',
            'http://flickr.com',
            'http://microsoft.com',
            'http://facebook.com',
            'http://twitter.com',
            'http://stuba.sk',
            'http://uim.fei.stuba.sk',
    ]:
        await work_queue.put(url)

    time_start = time.perf_counter()
    await asyncio.gather(
        task('One', work_queue),
        task('Two', work_queue),
    )
    elapsed = time.perf_counter() - time_start
    print(f'\n Total elapsed time: {elapsed:.1f}')


if __name__ == '__main__':
    asyncio.run(main())
