# sl 132 prednaska02
from fei.ppds import *
import random
from time import sleep


class SimpleBarrier:
    def __init__(self, N):
        self.N = N          # pocet vlaken ktore sa maju stretnut
        self.counter = 0    # pocitadlo vlaken
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)  # medzi R a KO
        # init na 1 aby nedoslo k deadlocku pri n-tom vlakne
        self.turnstile2 = Semaphore(1)  # medzi KO a R

    # na to aby sme osetrili predbiehanie sa vlaken, z dosledku N+1 volani bar.signal() pri jednorazovej bariere
    # potrebujeme 2 turnikety
    def barrier(self, id_t):
        self.mutex.lock()
        self.counter += 1
        # hodnota turnstile1 je urcite na konci cyklu 1
        # ak nie je v mutex, nevieme hodnotu, lebo vlakna sa mozu obiehat turnstile1 <1,N>
        if self.counter == self.N:
            print("n-te vlakno je ", id_t)
            print("turn2 zatvor", id_t)
            # aby sa pocet volani wait() a signal() zhodoval aj u turniketu2
            self.turnstile2.wait()      # zatvor 2. turniket   
            print("turn1 otvor", id_t)
            self.turnstile1.signal()    # otvor 1. turniket    
            #sleep(randint(1,10)/10) # ak zakomentovane, tak N-te vlakno vsetky predbehne
        self.mutex.unlock()

        # 1. bariera medzi R a KO
        print("turn1 caka vlakno", id_t) 
        self.turnstile1.wait()
        self.turnstile1.signal()

        # opravit N+1 signal() pridanim volania wait() - tiez ich bude N+1
        # prave jedno vlakno robi wait()
        self.mutex.lock()
        """# n-te vlakno robi dodatkovi wait()
        if self.counter == self.N:
            print("turn1 wait", id_t)
            self.turnstile1.wait()"""
        self.counter -= 1

        # posledne vlakno otvara za barieru za KO
        # zaroven posledne vlakno moze robit aj wait(), ktory chyba k N+1 signal() turniketu1 
        if self.counter == 0:
            # odpoved na otazku sl 116 p02
            # !!! t1.wait() a t2. signal() musi byt v takomto poradi
            # -> ak naopak tak by boli oba turnikety otvorene
            print("posledne vlakno", id_t)
            print("turn1 zatvor", id_t)
            self.turnstile1.wait()          # zatvor prvy turniket
            print("turn2 otvor", id_t)
            self.turnstile2.signal()        # otvor druhy turniket
        self.mutex.unlock()

        # 2. bariera medzi KO a R
        # vsetky vlakna cakaju za kritickou oblastou
        print("turn2 caka vlakno", id_t) 
        self.turnstile2.wait()
        self.turnstile2.signal()

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
        barrier.barrier(thread_name)
        ko(thread_name)
        # bariera pred randezvous
        barrier.barrier(thread_name)

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
