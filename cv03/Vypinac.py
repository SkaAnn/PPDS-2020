from fei.ppds import *

class Lightswitch:
    def __init__(self):
        # interny stav pocitadla
        self.mutex = Mutex()    # chrani integritu pocitadla
        self.counter = 0

    # p3b sl 93
    # lock() - zavola vlakno, ktore sa snazi dostat prve do miestnosti
    def lock(self, sem):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:   # prvy zazina
            sem.wait()
        self.mutex.unlock()

    # unlock() - posledne vlakno, ktore chce odist z miestnosti
    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:   # posledny zhasina
            sem.signal()
        self.mutex.unlock()
