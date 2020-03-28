# sl 93 prednaska03b
from fei.ppds import *
from time import sleep
from random import randint

# VYPINAC
class Lightswitch:
    def __init__(self):
        self.counter = 0        # pocitadlo vlakien, ktore su v miestnosti
        self.mutex = Mutex()    # chrani integritu pocitadla
    # 2 metody lock() a unlock() s argumentom semaforom

   
    # ZAZNI V MIESTNOSTI
    # Ak vlakno zavola metodu lock, a toto vlakno je prvym, ktore sa pokusa „dostat do miestnosti“,
    # nech vyvola nad semaforom, ktory je argumentom funkcie lock, operaciu wait()
    def lock(self, semaphore, id_t):
        self.mutex.lock()
        self.counter += 1       # vlakno prislo do miestnosti
        if self.counter == 1:   # prvy zazina v miestnosti
            print("ZAZLO vlakno", id_t)
            semaphore.wait()    # ked je nastaveny na 1 bude tam 0 -> miestnost je obsadena
        self.mutex.unlock()
    
    # ZHASNI V MIESTNOSTI
    # Ak vlakno zavola metodu unlock, a toto vlakno je poslednym, ktore sa pokusa „dostat z miestnosti“,
    # nech vyvola nad semaforom, ktory je argumentom funkcie unlock, operaciu signal()
    def unlock(self, semaphore, id_t):
        self.mutex.lock()
        self.counter -= 1       # vlakno odchadza z miestnosti
        if self.counter == 0:   # posledne vlakno zhasina v miestnosti
            print("ZHASLO vlakno", id_t)
            semaphore.signal()  # z 0 nastavi na 1 -> miestnost je znovu volna
        self.mutex.unlock() 

def test_fun(roomEmpty, ls, id_t):
    ls.lock(roomEmpty, id_t)
    sleep(randint(1,10)/10)
    print("vlakno", id_t,"vykonalo test_fun")
    ls.unlock(roomEmpty, id_t)   

def main():
    N = 5 # pocet vlaken
    sem = Semaphore(1)  # ak 1 tak miestnost je prazdna
    lsw = Lightswitch()
    threads = []
    
    for i in range(5):
        threads.append(Thread(test_fun, sem, lsw, i))

    for t in threads:
        t.join()
    

if __name__ == "__main__":
    main()
