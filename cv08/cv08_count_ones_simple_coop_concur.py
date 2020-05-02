# jednoducha kooperativna konkurencia
# implementacia vlastnej kooperativnej konkurencie = PRIMITIVNY PLANOVAC
# 1. task() zmenime na generator - prerusenie ulohy vyrazom yield, volame objekt generatora
# 2. riadiaci cyklus vyvolava ulohy, predava riadenie cez next()
# ulohy sa sami prerusia a dovolia beh dalsej ulohy
import queue
 
def task(name, queue):
    while not queue.empty():
        count = queue.get()
        print(f"Task {name} took value {count}")
        total = 0
        print(f"Task {name} running")
        for x in range(count):
            total += 1
            print(f"Task {name} yield! total: {total}")
            yield
        print(f"Task {name} total: {total}")

def main():
    work_queue = queue.Queue()
 
    # Do fronty dame objekty na spracovanie (cisla)
    for work in [15, 10, 5, 2]:
        work_queue.put(work)
 
    tasks = [task("One", work_queue), task("Two", work_queue)]
 
    # Spustime pripravene ulohy
    done = False
    while not done:
        for t in tasks:
            try:
                # task One si z fronty vytiahla 1. hodnotu
                # task Two si z fronty vytiahla 2. hodnotu 
                # task Two si z fronty vytiahla 3. hodnotu
                # task Two si z fronty vytiahla 4. hodnotu
                next(t)
            except StopIteration:
                # print(f"Task {t} was removed.")
                tasks.remove(t)
            if len(tasks) == 0:
                done = True
 
 
if __name__ == "__main__":
    main()
