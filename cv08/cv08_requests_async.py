# Written by Anton Caceres
# https://github.com/MA3STR0/PythonAsyncWorkshop

import asyncio
import aiohttp
import time
 
URLS = [
    'http://dsl.sk',
    'http://stuba.sk',
    'http://shmu.sk',
    'http://root.cz',
]

async def open_url(name, url):
    async with aiohttp.ClientSession() as session:
        print(f"Task {name} getting URL: {url}")
        time_start = time.perf_counter()
        async with session.get(url) as response:
                resp = await response.text()
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed:.1f}")
    return resp
 
async def request_greetings():
    # samotny for cyklus nemozem mat lebo by to znamenalo serializaciu
    # vrati list odpovedi
    responses = await asyncio.gather(*(open_url(i, URLS[i]) for i in range(len(URLS))))
    return responses
 
if __name__ == "__main__":
    t1 = time.time()
    # spusti funkciu
    greetings = asyncio.run(request_greetings())
    print(time.time() - t1, "seconds passed")
    print(greetings[0][0:250])
    #print(greetings)
