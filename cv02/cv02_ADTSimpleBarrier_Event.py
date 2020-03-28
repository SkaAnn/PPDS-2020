from fei.ppds import *
import random
import time

class SimpleBarrier:
    def __init__(self, N):
        self.N = N          # pocet vlaken ktore sa maju stretnut
        self.counter = 0    # pocitadlo vlaken
        self.mutex = Mutex()
        self.bar = Event() # bariera/zabrana na ktorej vlakna cakaju
 
    def barrier(self, id_t):
        # vlakno prislo k bariere zvys pocitadlo
        self.mutex.lock()
        self.counter += 1
        self.mutex.unlock()
        # ak je to vlakno posledne tak pusti cakajuce
        if self.counter == self.N:
            print("n-te vlakno je", id_t)
            print("bar signal", id_t)
            # signal() odblokuje vsetky vlakna cakajuce na wait()
            self.bar.signal()
            
        # inak cakaj na zabrane
        # KO sa nesmie vykonat pokym sa nestretnu/nepridu vsetky vlakna
        # prve volanie wait() po signal() nie je blokujuce (cize N-te vlakno bezproblemov prejde)
        self.bar.wait()
        # aby sa bariera po prechode N vlaken zavrela (treba zmazat vzn. udalost)
        self.bar.clear()
        
               
# predpokladajme, ze nas program vytvara a spusta 5 vlakien,
# ktore vykonavaju nasledovnu funkciu, ktorej argumentom je
# zdielany objekt jednoduchej bariery
def barrier_example(barrier, thread_id):
    time.sleep(randint(1,10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.barrier(thread_id)
    print("vlakno %d po bariere" % thread_id)

def main():
    # zdielany objekt bariery
    # priklad pouzitia ADT SimpleBarrier
    barrier = SimpleBarrier(5)
     
    # vytvara a spusta 5 vlakien
    # Thread - funkcia ktoru vykonava, argumenty funkcie
    threads = []
    for i in range(5):
        threads.append(Thread(barrier_example, barrier, i))

    for i in range(5):
        threads[i].join()

if __name__ == "__main__":
    main()
