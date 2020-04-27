#!/usr/bin/env python3

from fei.ppds import Thread, Mutex, Semaphore, Event, print
from time import sleep
from random import randint


class Shared(object):
    def __init__(self, N):
        self.N = N
        self.customers = 0
        self.queue = []
        self.mutex = Mutex()
        self.customer = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barberDone = Semaphore(0)


def getHairCut(cid):
    print(f"customer {cid} getHairCut")
    sleep(randint(0,10)/100)


def cutHair():
    print(f"barber cutHair")
    sleep(randint(0,10)/100)


def balk(cid):
    print(f"customer {cid} balk")


def customer(shared, cid):
    barber = Semaphore(0)

    while True:
        sleep(randint(9,10)/100)

        shared.mutex.lock()
        if shared.customers == shared.N:
            balk(cid)
            shared.mutex.unlock()
            continue
        print(f"customer {cid} wait for...")
        shared.queue.append(barber)
        shared.customers += 1
        shared.mutex.unlock()

        shared.customer.signal()
        barber.wait()
        getHairCut(cid)
        shared.customerDone.signal()
        shared.barberDone.wait()

        shared.mutex.lock()
        shared.customers -= 1
        shared.mutex.unlock()


def barber(shared):
    while True:
        shared.customer.wait()
        shared.mutex.lock()
        barber = shared.queue.pop(0)
        shared.mutex.unlock()
        barber.signal()
        cutHair()
        shared.customerDone.wait()
        shared.barberDone.signal()

    
def run_model():
    shared = Shared(5)

    b = Thread(barber, shared)
    customers = [Thread(customer, shared, i) for i in range(10)]

    
if __name__ == "__main__":
    run_model()
