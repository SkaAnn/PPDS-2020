from fei.ppds import Thread, Semaphore, Mutex, print
from random import randint
from time import sleep
 
# vypisovat na monitor budeme pomocou funkcie 'print'
# importovanej z modulu 'ppds'
# to kvoli tomu, aby neboli 'rozbite' vypisy

##### PREDNASKA 2 sl 78
class SimpleBarrier:
    def __init__(self, N):
        self.N = N                  # pocet vlaken, ktore budu cakat
        self.counter = 0            # premenna, ktora rata pocet vlaken, co cakaju
        self.mutex = Semaphore(1)   # Semaphor inicializovany na 1 je to iste co Mutex
        self.barriera = Semaphore(0)#
        
    def barrier(self):
        # vlakno prislo ku bariere, zvys counter ze prislo
        # v jednom case moze inkrementovat counter iba jedno vlakno
        self.mutex.wait()
        self.counter += 1
        self.mutex.signal()
        # ak prisli vsetky vlakna k bariere otvor ju a pusti prveho...
        # to co dojde posledne aj prve vyjde (?)
        if self.counter == self.N:
            self.barriera.signal()
        # inak budu vlakna cakat
        self.barriera.wait()
        # pustene vlakno pusti dalsie
        self.barriera.signal()
        
 
# priklad pouzitia ADT SimpleBarrier
t = SimpleBarrier(5)
 
# predpokladajme, ze nas program vytvara a spusta 5 vlakien,
# ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
# zdielany objekt jednoduchej bariery
def barrier_example(barrier, thread_id):
    sleep(randint(1,10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.barrier()
    print("vlakno %d po bariere" % thread_id)

 
##### MAIN
# kod, v ktorom sa vytvara a spusta 5 vlakien
threads = []
for i in range(5):
    # prvy argument funkcia, ktoru ma vlakno vykonavat
    # dalsie 2 argumenty patria funkcii barrier_example - barrier, thread_id
    threads.append(Thread(barrier_example, t, i))

# spusti vlakna
for i in range(5):
    threads[i].join()

