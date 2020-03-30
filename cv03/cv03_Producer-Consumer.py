# sl 59 prednaska03b
# PRODUCENT A KONZUMENT
from fei.ppds import *
from time import sleep

# zdielany objekt pre producenta aj konzumenta
class Shared:
    def __init__(self, N):          # N je kapacita skladu
        self.mutex = Mutex()        # chrani integritu operacii so skladom
        self.items = Semaphore(0)   # pocet poloziek, ktore mozu zakaznici kupit
        self.free = Semaphore(N)    # pocet poloziek, ktore mozu dodavatelia dodat

def produce(shared,id_t):
    while True:
        # produkovanie polozky pred tym ako zistime ci mozme hned dodat (lebo vytvaranie moze trvat prilis dlho)
        sleep(randint(1,10)/10)  # 1. cas produkcie vyrobku
        # print("vlakno",id_t,"vytvorilo polozku") 
        # producent nesmie dodat polozku do plneho skladu !!! (items=buffer.size, free=0)
        shared.free.wait() # producent chce dodat polozku
        # shared.mutex.lock()
        # dodavanie polozky do buffra
        print("vlakno",id_t,"dodalo polozku")
        # shared.mutex.unlock()
        shared.items.signal()      # polozka bola dodana

def consume(shared, id_t):
    while True:
        # konzument nesmie zobrat polozku z prazdneho skladu !!! (items=0, free=buffer.size)
        shared.items.wait()
        # shared.mutex.lock()
        # zoberie polozku z buffra
        # print("vlakno",id_t,"zobralo polozku")
        # shared.mutex.unlock()
        shared.free.signal()   # polozka zobrana zo skladu (mozme ju dodat)
        sleep(randint(1,10)/10)  # 2. cas spracovania vyrobku
        print("vlakno",id_t,"skonzumovalo polozku")
    

def main():
    sh = Shared(10)     # kapacita skladu je 10
    producers = []
    consumers = []
    
    for i in range(3):  # 3 dodavatelia
        producers.append(Thread(produce, sh, i))
    for i in range(3,10):   # 7 zakaznikov
        consumers.append(Thread(consume, sh, i))
        
    for t in producers:
        t.join()       
    for t in consumers:
        t.join()

if __name__ == "__main__":
    main()
        
