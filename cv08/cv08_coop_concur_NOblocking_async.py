# ASYNCHRONNY KOD
# kooperativna konkurencia s neblokujucimi volaniami
# treba:    1. async def funkcie
#           2. await prerusenie behu ulohy, prenechanie behu inym uloham
#           3. asyncio.run() event loop
import asyncio
import time

# funkcia task oznacena async = nativna korutina
async def task(name, queue):
    while not queue.empty():
        delay = await queue.get()
        print(f"Task {name} running")
        time_start = time.perf_counter()
        # neblokujuce volanie sleep
        await asyncio.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed:.1f}")
 
 
async def main():
    # Create the queue of work
    work_queue = asyncio.Queue()
 
    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        # miesto kde vieme funkciu prerusit
        await work_queue.put(work)  # musi byt await inak chyba - kazda korutina musi byt await

 
    start_time = time.perf_counter()
    # spustanie uloh - najprv vytvori objekty (naplanuje ich) a potom konkurentne spusti
    # bezia 2 korutiny konkurentne
    await asyncio.gather(
        task("One", work_queue),    # vytvori objekt korutiny
        task("Two", work_queue),
    )
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")
    # Vysledok je taky, aky je cas trvania pre dokoncenie ulohy poslednej z korutin
 
 
if __name__ == "__main__":
    asyncio.run(main())
