# sl 100 prednaska03b
# vyhladovenie zapisovatelov
from fei.ppds import *
from time import sleep
from random import randint

class Lightswitch():
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):  
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:   # 1. zazina v miestnosti
            sem.wait()
        self.mutex.unlock()

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:   # posledny zhasina v miestnosti
            sem.signal()
        self.mutex.unlock()

class Shared():
    def __init__(self):
        self.room_empty = Semaphore(1)  # 1 zapisovatel moze zapisovat
        self.readLS = Lightswitch()     # viacery citatelia mozu citat
        
def reader_thread(thread_id, shared):
    while True:
        # pred kazdym pokusom o precitanie pocka v intervale <0.0; 1> sekundy
        sleep(0.5+randint(0, 10)/10)
        shared.readLS.lock(shared.room_empty)
        # simulacia dlzky citania v intervale <0.5; 0.9> sekundy
        sleep(0.5 + randint(0, 4)/10)
        print(thread_id,"cital") 
        shared.readLS.unlock(shared.room_empty)
    

def writer_thread(thread_id, shared):
    while True:
        # pred kazdym pokusom o zapis pocka v intervale <0.0; 1> sekundy
        sleep(randint(0, 10)/10)
        shared.room_empty.wait()
        # simulujeme dlzku zapisu v intervale <0.3; 0.7> sekundy
        sleep(0.3 + randint(0, 4)/10)
        print(thread_id,"zapisal")
        shared.room_empty.signal()

# nastane vyhladovenie zapisovatelov (nedostanu sa k slovu...)
# kvoli nepomeru vlaken
# alebo roznej dobe citania a zapisu vzhladom na pocet vlaken
def main():
    """
    Vytvorime vlakna, ktore chceme synchronizovat.
    Nezabudnime vytvorit aj zdielane synchronizacne objekty,
    a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
    synchronizovat.
    """
     
    shared = Shared()
    threads = []
     
    for i in range(5):
        t = Thread(writer_thread, "Writer %d" % i, shared)
        threads.append(t)
    for i in range(10):
        t = Thread(reader_thread, "Reader %d" % i, shared)
        threads.append(t)
        
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
