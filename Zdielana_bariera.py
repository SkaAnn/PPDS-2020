from time import sleep
from random import randint
from ppds import Thread, Mutex, Semaphore, Event, print

class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.count = 0
        self.m = Mutex()
        #self.m = Semaphore(1)   # mutex
        self.b = Event()         # barier
 
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

# 2 cakania - 2 turnikety
def barrier(thread_name, SiBa):
    while True:
        # ...
        rendezvous(thread_name)
        # ...

        # zvys counter ze prislo vlakno

        SiBa.count += 1
        print(SiBa.count)

        # spocitaj ze kolko je vlaken predtym ako vykonas funkciu ko
        if counter == SiBa.N:
            SiBa.b.signal()
        SiBa.b.wait()
            
        ko(thread_name)
        # ...
 
 
"""
Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""

sb = SimpleBarrier(10)
threads = list()
for i in range(10):
    t = Thread(barrier, 'Thread %d' % i, sb)
    threads.append(t)
 
for t in threads:
    t.join()
