from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self, last_signal: Semaphore):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0             # posledne vlakno nastavi pocitadlo na nulu
            last_signal.signal()
            self.T.signal(self.N)  # uvolni N vlakien
        self.M.unlock()
        self.T.wait()



class Shared:
    def __init__(self, c, m):
        self.c = c
        self.m = m
        self.board_queue = Semaphore(0)
        self.unboard_queue = Semaphore(0)
        self.barrier = SimpleBarrier(c)
        self.changed = Semaphore(0)
        self.loading_area = [Semaphore(0) for i in range(m)]
        self.unloading_area = [Semaphore(0) for i in range(m)]

    def next_car(self, i):
        return (i + 1) % self.m


def load(id_car):
    print(f'train {id_car} loading passengers')


def run(id_car):
    print(f'train {id_car} running!!!')
    sleep(randint(50, 300) / 100)


def unload(id_car):
    print(f'train {id_car} unloading passengers')


def board(id_pass):
    print(f'passenger {id_pass} boarded')
    sleep(randint(50, 200) / 100)


def unboard(id_pass):
    print(f'passenger {id_pass} unboarded')
    sleep(randint(50, 200) / 100)


def car(s, id_car):
    while True:
        s.loading_area[id_car].wait()
        load(id_car)
        s.board_queue.signal(s.c)
        s.changed.wait()
        s.loading_area[s.next_car(id_car)].signal()

        run(id_car)

        s.unloading_area[id_car].wait()
        unload(id_car)
        s.unboard_queue.signal(s.c)
        s.changed.wait()
        s.unloading_area[s.next_car(id_car)].signal()


def passenger(s, id_pass):
    while True:
        s.board_queue.wait()
        board(id_pass)
        s.barrier.wait(s.changed)

        s.unboard_queue.wait()
        unboard(id_pass)
        s.barrier.wait(s.changed)


def main():
    c = 4
    m = 3
    s = Shared(c, m)
    for i in range(15):
        Thread(passenger, s, i)
    for i in range(m):
        Thread(car, s, i)
    s.loading_area[0].signal()
    s.unloading_area[0].signal()


if __name__ == '__main__':
    main()
