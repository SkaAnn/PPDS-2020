from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0             # posledne vlakno nastavi pocitadlo na nulu
            self.T.signal(self.N)  # uvolni N vlakien
        self.M.unlock()
        self.T.wait()


class Shared:
    def __init__(self):
        self.hackers = 0
        self.serfs = 0
        self.mutex = Mutex()
        self.hackers_queue = Semaphore(0)
        self.serfs_queue = Semaphore(0)
        self.barrier = SimpleBarrier(4)


def board(who, id_):
    print(f'{who} {id_} boarded')
    sleep(randint(50, 300) / 100)


def row_boat(who, id_):
    print(f'{who} {id_} rowing!!!')
    sleep(randint(50, 300) / 100)


def hacker(s, id_hacker):
    is_captain = False
    while True:
        s.mutex.lock()
        s.hackers += 1
        if s.hackers == 4:
            is_captain = True
            s.hackers = 0
            s.hackers_queue.signal(4)
        elif s.hackers == 2 and s.serfs >= 2:
            is_captain = True
            s.hackers = 0
            s.serfs -= 2
            s.hackers_queue.signal(2)
            s.serfs_queue.signal(2)
        else:
            s.mutex.unlock()

        # cakanie na brehu
        s.hackers_queue.wait()
        board('hacker', id_hacker)
        s.barrier.wait()

        if is_captain:
            row_boat('hacker', id_hacker)
            is_captain = False
            s.mutex.unlock()


def serf(s, id_serf):
    is_captain = False
    while True:
        s.mutex.lock()
        s.serfs += 1
        if s.serfs == 4:
            is_captain = True
            s.serfs = 0
            s.serfs_queue.signal(4)
        elif s.serfs == 2 and s.hackers >= 2:
            is_captain = True
            s.serfs = 0
            s.hackers -= 2
            s.hackers_queue.signal(2)
            s.serfs_queue.signal(2)
        else:
            s.mutex.unlock()

        # cakanie na brehu
        s.serfs_queue.wait()
        board('serf', id_serf)
        s.barrier.wait()

        if is_captain:
            row_boat('serf', id_serf)
            is_captain = False
            s.mutex.unlock()


def main():
    s = Shared()
    for i in range(5):
        Thread(hacker, s, i)
        Thread(serf, s, i)


if __name__ == '__main__':
    main()
