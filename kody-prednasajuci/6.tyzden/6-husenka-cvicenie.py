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
    def __init__(self, c):
        self.c = c
        self.board_queue = Semaphore(0)
        self.unboard_queue = Semaphore(0)
        self.barrier = SimpleBarrier(c)
        self.changed = Semaphore(0)


def load():
    print('train loading passengers')


def run():
    print('train running!!!')
    sleep(randint(50, 300) / 100)


def unload():
    print('train unloading passengers')


def board(id_pass):
    print(f'passenger {id_pass} boarded')
    sleep(randint(50, 200) / 100)


def unboard(id_pass):
    print(f'passenger {id_pass} unboarded')
    sleep(randint(50, 200) / 100)


def car(s):
    while True:
        load()
        s.board_queue.signal(s.c)
        s.changed.wait()

        run()

        unload()
        s.unboard_queue.signal(s.c)
        s.changed.wait()


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
    s = Shared(c)
    for i in range(5):
        Thread(passenger, s, i)
    Thread(car, s)


if __name__ == '__main__':
    main()
