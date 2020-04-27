async def produce(n: int, q: asyncio.Queue) -> None:
    # Synchronous loop for each single producer
    for _ in range(n):
        item = await makeitem()
        await q.put(item)

async def consume(q: asyncio.Queue) -> None:
    while True:
        item = await q.get()
        await consume_item(item)
        q.task_done()

async def main(nprod: int, ncon: int) -> None:
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    asyncio.run(main(3,10))
