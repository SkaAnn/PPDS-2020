from fei.ppds import *
import time

# problem Producent-Konzument implementovany cez vypinac
# p3b sl 54 P-K
# normalne parametre 4xcas + pocet konzumentov + pocet producentov + velkost buffra
# zavislost coho od coho chceme pozorovat

class Produce_Consume():
    def __init__(self, buff_size):
        self.mutex = Mutex()
        self.items = Semaphore(0)
        self.free = Semaphore(buff_size)

    def produce(self, id):
        for i in range(5):
            time.sleep(0.1) # nahradzuje item=produceItem()
            print("producent", id, "vytvoril polozku")
            self.mutex.lock()
            time.sleep(0.2)
            print("producent", id, "pridal polozku")
            self.mutex.unlock()
            self.items.signal()
        
    def consume(self, id):
        for i in range(5):
            self.items.wait()
            self.mutex.lock()
            time.sleep(0.1)
            print("konzument", id, "odobral polozku")
            self.mutex.unlock()
            time.sleep(0.2)
            print("konzument", id, "konzumoval polozku")

pc = Produce_Consume(5)
producers = []
consumers = []
for i in range(5):
    producers.append(Thread(pc.produce, i))
    consumers.append(Thread(pc.consume, i))
    
for th in producers:
    th.join()
for th in consumers:
    th.join()
    
