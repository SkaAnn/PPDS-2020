# PODMIENKY
# 1. v jednom case iba 1 vidlicku (1 vidlicku nemozu mat naraz viacery filozofi)
# 2. nenastal deadlock
# 3. nenastalo vyhladovenie niektoreho filozofa (vlakno sa nedostane k slovu)
# 4. mohli jest viaceri filozofi sucasne
from fei.ppds import *
from time import sleep
from random import randint

class Shared():
    def __init__(self, N):
        self.N = N  # pocet vecerajucich filozofov
        # semafor pre kazdu vidlicku (je/nie je obsadena)
        self.forks = [Semaphore(1) for i in range(N)]
    
    def right(self, i):
        return i

    def left(self, i):
        return (i+1)%self.N

# zober vidlicku (zniz semafor)
def get_forks(shared, i):   # i je pozicia filozofa
    ind_l = shared.left(i)
    shared.forks[shared.right(i)].wait()
    shared.forks[shared.left(i)].wait()
    print("Filozof", i, "zobral vidlicku", i,"a", ind_l)

# poloz vidlicku (zvys semafor)
def put_forks(shared, i):
    ind_l = shared.left(i)
    shared.forks[shared.right(i)].signal()
    shared.forks[shared.left(i)].signal()
    print("Filozof", i, "polozil vidlicku", i,"a", ind_l)

def think(id_t):
    print("Filozof",id_t,"prave premysla")
    sleep(randint(2, 5)/10)

# na splnenie podm 3. musi fun skoncit v konecnom case
def eat(id_t):
    print("Filozof", id_t, "prave veceria")
    sleep(randint(5, 10)/10)
    print("Filozof", id_t, "dojedol")
    pass

def eating_dinner(shared, id_t):
    while True:
        think(id_t)
        get_forks(shared, id_t)
        eat(id_t)
        put_forks(shared, id_t)

def main():
    N = 5
    sh = Shared(N)
    threads = []
     
    for i in range(N):
        t = Thread(eating_dinner, sh, i)
        threads.append(t)
     
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
