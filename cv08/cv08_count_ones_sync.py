# vybera z fronty data na spracovanie (cele cisla)
# a po ich vybrati spocita tolko jednotiek kolko je hodnota vybraneho cisla
# ak je fronta prazdna uloha sa ukonci

import queue
 
def task(name, work_queue):
    if work_queue.empty():
        print(f"Task {name} nothing to do")
    else:
        while not work_queue.empty():
            count = work_queue.get()
            total = 0
            print(f"Task {name} running")
            for x in range(count):
                total += 1
            print(f"Task {name} total: {total}")
 
def main():
    work_queue = queue.Queue()
 
    # Do fronty dame objekty na spracovanie (cisla)
    for work in [15, 10, 5, 2]:
        work_queue.put(work)
 
    # Pripravime dve synchronne ulohy
    tasks = [(task, "One", work_queue), (task, "Two", work_queue)]
 
    # Spustime pripravene ulohy
    for t, n, q in tasks:
        t(n, q)

    # Task One spracovala vsetky udaje z fronty, lebo sa prva chopila ulohy.
    # Task Two nemala co spracovat. 
 
if __name__ == "__main__":
    main()
    
