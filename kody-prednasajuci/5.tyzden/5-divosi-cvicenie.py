from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class Shared:
    def __init__(self, n):
        self.servings = n
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

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
        s.mutex.lock()
        if s.servings == 0:
            print(f'savage {savage_id} signalling cook')
            s.empty_pot.signal()
            s.full_pot.wait()
        s.get_serving_from_pot(savage_id)
        s.mutex.unlock()
        eat(savage_id)


def cook(s):
    while True:
        s.empty_pot.wait()
        print('cook cooking')
        sleep(randint(50, 200) / 100)
        print('cook: adding servings to the pot')
        s.put_servings_to_pot(10)
        s.full_pot.signal()


def main():
    s = Shared(0)
    for i in range(10):
        Thread(savage, i, s)
    Thread(cook, s)


if __name__ == '__main__':
    main()
