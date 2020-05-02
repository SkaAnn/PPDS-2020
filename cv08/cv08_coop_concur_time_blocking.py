# kooperativna konkurencia s blokujucimi volaniami
# blokujuce volanie = time.sleep()
# blokujuce volanie sposobi ze procesor prestane vykonavat kod programu a caka kym nepride odpoved z volania
# + meranie casu: dlzka 1 ulohy, celkova dlzka behu uloh

import time
import queue
 
 
def task(name, queue):
    while not queue.empty():
        delay = queue.get()
        print(f"Task {name} running")
        time_start = time.perf_counter()
        # ani tu nic nepomoze yield
        time.sleep(delay)   # BLOKUJUCE VOLANIE
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed:.1f}")
        yield # ULOHY PRED BLOKOVANIM NEODOVZDALI RIADENIE! takze sme nic neziskali...
 
def main():
    # Create the queue of work
    work_queue = queue.Queue()
 
    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)
 
    tasks = [task("One", work_queue), task("Two", work_queue)]
 
    # Run the tasks
    done = False
    start_time = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
                if len(tasks) == 0:
                    done = True
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed:.1f}")
 
 
if __name__ == "__main__":
    main()
