from Vypinac import *
import time

def Vypinac_test(vyp, sem, thread_id):
    vyp.lock(sem)
    print("toto je vlakno medzi lock a unlock ", thread_id)
    time.sleep(0.5)
    vyp.unlock(sem)
    

sem = Semaphore(1)
ls = Lightswitch()

threads = []
for i in range (5):
    threads.append(Thread(Vypinac_test, ls, sem, i))

for i in range (5):
    threads[i].join()
