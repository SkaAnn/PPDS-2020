# sl 146, 147 prednaska02
from fei.ppds import *
import random
from time import sleep
 
class SimpleBarrier:
    def __init__(self, N):
        self.N = N          # pocet vlaken ktore sa maju stretnut
        self.counter = 0    # pocitadlo vlaken
        self.mutex = Mutex()
        self.bar = Semaphore(0) # bariera/zabrana na ktorej vlakna cakaju
 
    def barrier(self, id_t):
        self.mutex.lock()
        self.counter += 1
        # ak je to vlakno posledne tak pusti cakajuce
        if self.counter == self.N:
            print("n-te vlakno je", id_t)
            self.counter = 0        # vynuluj counter
            self.bar.signal(self.N) # pusti N vlaken
        self.mutex.unlock()
        self.bar.wait()

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

# ZNOVOPOUZITELNA BARIERA POMOCOU 2 JEDNODUCHYCH BARIER 
"""
Kazde vlakno vykonava kod funkcie 'barrier'.
Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
nielen pred vykonanim funkcie 'ko', ale aj
*vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
"""
def barrier_example(barrier1, barrier2, thread_name):
    while True:
        rendezvous(thread_name)
        # 1. bariera R-KO
        sleep(randint(1,10)/10)
        print("vlakno %d pred 1. barierou" % thread_name)
        barrier1.barrier(thread_name)
        print("vlakno %d po 1. bariere" % thread_name)

        ko(thread_name)
        # 2. bariera KO-R
        print("vlakno %d pred 2. barierou" % thread_name)
        barrier2.barrier(thread_name)
        print("vlakno %d po 2. bariere" % thread_name)

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
        t = Thread(barrier_example, bar1, bar2, i) #'Thread %d' % i)
        threads.append(t)
     
    for t in threads:
        t.join()
        
if __name__ == "__main__":
    main()
