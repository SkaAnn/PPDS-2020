from time import sleep
from random import randint
from fei.ppds import *

class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.bar = Event()

    def barrier(self, id_t):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            print("n-te vlakno je", id_t)
            self.bar.signal()
            sleep(0.1) # v pripade ze prve vlakno spusta clear(),
            # tak toto vlakno by mohlo zaspat udalost a nastal by deadlock
        self.mutex.unlock()
        
        self.bar.wait()
        # kvoli moznemu deadlocku musi spustat clear() posledne vlakno!
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            self.bar.clear()
        self.mutex.unlock()
        
"""
Vypisovat na monitor budeme pri zamknutom mutexe pomocou
funkcie 'print' z modulu 'ppds', aby sme nemali rozbite vypisy.
"""
 
def rendezvous(thread_name):
    sleep(randint(1,10)/10)
    print('rendezvous: %s' % thread_name)
 
def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1,10)/10)
 
"""
Kazde vlakno vykonava kod funkcie 'barrier'.
Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
nielen pred vykonanim funkcie 'ko', ale aj
*vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
"""
def barrier(barrier1, barrier2, thread_name):
    while True:
        rendezvous(thread_name)
        barrier1.barrier(thread_name)
        ko(thread_name)
        barrier2.barrier(thread_name)
 
def main():
    bar1 = SimpleBarrier(10)
    bar2 = SimpleBarrier(10)
    """
    Vytvorime vlakna, ktore chceme synchronizovat.
    Nezabudnime vytvorit aj zdielane synchronizacne objekty,
    a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
    synchronizovat.
    """
    threads = list()
    for i in range(10):
        t = Thread(barrier, bar1, bar2, 'Thread %d' % i)
        threads.append(t)
     
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
