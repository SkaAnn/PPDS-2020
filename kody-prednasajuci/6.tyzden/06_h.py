#!/usr/bin/env python3

from fei.ppds import Thread, Mutex, Semaphore, Event, print
from time import sleep
from random import randint, choice


class Barrier(object):
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.b1 = Semaphore(0)
        self.b2 = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            print("------")
            self.b1.signal(self.N)
        self.mutex.unlock()
        self.b1.wait()

        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            self.b2.signal(self.N)
        self.mutex.unlock()
        self.b2.wait()


class Shared(object):
    def __init__(self):
        self.oxygen = 0
        self.hydrogen = 0
        self.mutex = Mutex()
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)
        self.barrier = Barrier(3)


def bond(mid):
    print(f"bond {mid}")


def oxygen(shared):
    shared.mutex.lock()
    shared.oxygen += 1
    if shared.hydrogen < 2:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)
        shared.hydroQueue.signal(2)

    shared.oxyQueue.wait()
    bond(oxygen.mid)
    shared.barrier.wait()

    shared.mutex.unlock()


def hydrogen(shared):
    shared.mutex.lock()
    shared.hydrogen += 1
    if shared.oxygen < 1 or shared.hydrogen < 2:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)
        shared.hydroQueue.signal(2)

    shared.hydroQueue.wait()
    bond(hydrogen.mid)
    shared.barrier.wait()

    
def run_model():
    oxygen.mid = 'O'
    hydrogen.mid = 'H'
    shared = Shared()

    while True:
        Thread(choice([oxygen,hydrogen]), shared)
        sleep(randint(0,3)/100)

    
if __name__ == "__main__":
    run_model()
