from ppds import Thread, Semaphore, Mutex, print
from random import randint
from time import sleep
 
# vypisovat na monitor budeme pomocou funkcie 'print'
# importovanej z modulu 'ppds'
# to kvoli tomu, aby neboli 'rozbite' vypisy
 
class SimpleBarrier:
    #### sl 78
    def __init__(self, N):
        self.N = N
        self.count = 0
        self.m = Mutex()
        #self.m = Semaphore(1)   # mutex
        self.b = Semaphore(0)   # barier
    
    def barrier(self):
        #self.m.wait()
        self.m.lock()
        self.count += 1
        #self.m.signal()
        self.m.unlock()
        if self.count == self.N:
            self.b.signal()
        self.b.wait()
        self.b.signal()
 
# priklad pouzitia ADT SimpleBarrier
# vytvori barieru pre 5 vlaken
t = SimpleBarrier(5)
 
# predpokladajme, ze nas program vytvara a spusta 5 vlakien,
# ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
# zdielany objekt jednoduchej bariery
def barrier_example(barrier, thread_id):
    sleep(randint(1,10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.barrier()
    print("vlakno %d po bariere" % thread_id)
 
# doplnit kod, v ktorom sa vytvara a spusta 5 vlakien
# ...
# vlakno vykonava funkciu barier_example - 1. argument
# ostatne argumenty su vstupy do funkcie
v1 = Thread(barrier_example, t, 1)
v2 = Thread(barrier_example, t, 2)
v3 = Thread(barrier_example, t, 3)
v4 = Thread(barrier_example, t, 4)
v5 = Thread(barrier_example, t, 5)

v1.join()
v2.join()
v3.join()
v4.join()
v5.join()


