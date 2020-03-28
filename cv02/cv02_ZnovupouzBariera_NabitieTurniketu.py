# sl 141 prednaska02
from fei.ppds import *
import random
from time import sleep

# DVOJFAZOVA BARIERA
# pomocou nabijania turniketu
class DoubleBarrier:
    def __init__(self, N):
        self.N = N          # pocet vlaken ktore sa maju stretnut
        self.counter = 0    # pocitadlo vlaken
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)  # medzi R a KO
        # MUSI BYT NULA!!! (lebo tu je presne tolko volani wait kolko signal)
        self.turnstile2 = Semaphore(0)  # medzi KO a R

    # mame moznost zvysit hodnotu semaforu na N
    # cize pocet volani signal() == wait() !!!
    def barrier_RKO(self, id_t):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:  # n-te vlakno odomyka 1. turniket 
            # pusti N vlaken
            print("n-te vlakno", id_t)
            self.turnstile1.signal(self.N)  # turn1 sa automaticky zavrie po prejdeni N vlaken
        self.mutex.unlock()
        # 1. bariera medzi R a KO
        print("turn1 wait", id_t)
        self.turnstile1.wait()
        print("turn1 go", id_t)

    def barrier_KOR(self, id_t):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:   # posledne vlakno odomyka 2. turniket
            print("posledne vlakno", id_t)
            self.turnstile2.signal(self.N) # turn2 sa automaticky zavrie po prejdeni N vlaken
        self.mutex.unlock()
        # 2. bariera medzi KO a R
        print("turn2 wait", id_t)
        self.turnstile2.wait()
        print("turn2 go", id_t)

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
        rendezvous(thread_name)
        # bariera pred ko
        barrier.barrier_RKO(thread_name)
        ko(thread_name)
        # bariera pred randezvous
        barrier.barrier_KOR(thread_name)

def main():
    """
    Vytvorime vlakna, ktore chceme synchronizovat.
    Nezabudnime vytvorit aj zdielane synchronizacne objekty,
    a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
    synchronizovat.
    """
    bar = DoubleBarrier(10)

    threads = list()
    for i in range(10):
        t = Thread(barrier_example, bar, 'Thread %d' % i)
        threads.append(t)
     
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
