# sl 132 prednaska02
from fei.ppds import *
import random
from time import sleep
 
class SimpleBarrier:
    def __init__(self, N):
        self.N = N          # pocet vlaken ktore sa maju stretnut
        self.counter = 0    # pocitadlo vlaken
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)

    # na to aby sme osetrili predbiehanie sa vlaken, z dosledku N+1 volani bar.signal() pri jednorazovej bariere
    # potrebujeme 2 turnikety
    def barrier(self, id_t):
        self.mutex.lock()
        self.counter += 1
        # hodnota turnstile1 je urcite na konci cyklu 1
        # ak nie je v mutex, nevieme hodnotu, lebo vlakna sa mozu obiehat turnstile1 <1,N>
        if self.counter == self.N:
            print("n-te vlakno je ", id_t)
            print("turn1 signal2", id_t)
            self.turnstile1.signal()
            sleep(randint(1,10)/10) # musi byt, inak N-te vlakno vsetky predbehne
        self.mutex.unlock()

        print("turn1 wait1", id_t)
        self.turnstile1.wait()
        print("turn1 signal1", id_t)
        self.turnstile1.signal()

        # opravit N+1 signal() pridanim volania wait()
        # prave jedno vlakno robi wait
        self.mutex.lock()
        if self.counter == self.N:
            print("turn1 wait2", id_t)
            self.turnstile1.wait()
            self.counter -= 1
        self.mutex.unlock()

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
def barrier_example(barrier, thread_name):
    while True:
        # bariera pred randezvous
        # ...
        rendezvous(thread_name)
        # bariera pred ko
        barrier.barrier(thread_name)
        ko(thread_name)
        # ...
 

def main():
    """
    Vytvorime vlakna, ktore chceme synchronizovat.
    Nezabudnime vytvorit aj zdielane synchronizacne objekty,
    a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
    synchronizovat.
    """
    bar = SimpleBarrier(10)

    threads = list()
    for i in range(10):
        t = Thread(barrier_example, bar, 'Thread %d' % i)
        threads.append(t)
     
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
