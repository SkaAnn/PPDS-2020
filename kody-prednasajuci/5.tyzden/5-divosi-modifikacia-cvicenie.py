from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self, savage_id, barrier_id):
        self.M.lock()
        self.C += 1
        print(f'savage {savage_id} before barrier {barrier_id}, {self.C} present')
        if self.C == self.N:
            print(f'savage {savage_id} opening barrier {barrier_id}')
            self.C = 0             # posledne vlakno nastavi pocitadlo na nulu
            self.T.signal(self.N)  # uvolni N vlakien
        self.M.unlock()
        self.T.wait()


class Shared:
    def __init__(self, n, n_savages):
        self.servings = n
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(n_savages)
        self.barrier2 = SimpleBarrier(n_savages)

    def get_serving_from_pot(self, savage_id):
        print(f'savage {savage_id}: taking a portion')
        self.servings -= 1

    def put_servings_to_pot(self, n):
        self.servings += n


def eat(savage_id):
    print(f'savage {savage_id}: eating a portion')
    sleep(randint(50, 200) / 100)


def savage(savage_id, s):
    while True:
        s.barrier1.wait(savage_id, 1)
        s.mutex.lock()
        if s.servings == 0:
            print(f'savage {savage_id} signalling cook')
            s.empty_pot.signal()
            s.full_pot.wait()
        s.get_serving_from_pot(savage_id)
        s.mutex.unlock()
        eat(savage_id)
        s.barrier2.wait(savage_id, 2)


def cook(s):
    while True:
        s.empty_pot.wait()
        print('cook cooking')
        sleep(randint(50, 200) / 100)
        print('cook: adding servings to the pot')
        s.put_servings_to_pot(3)
        print("pocet porcii", s.servings)
        s.full_pot.signal()


def main():
    n_savages = 5
    s = Shared(0, n_savages)
    for i in range(n_savages):
        Thread(savage, i, s)
    Thread(cook, s)


if __name__ == '__main__':
    main()
