from fei.ppds import *

# zdielany objekt vyjadreny triedou Shared
class Shared:
    # atributy triedy
    def __init__(self, n):
        self.counter = 0    # spolocne pocitadlo
        self.end = n        # velkost pola
        self.elms = [0]*n   # celociselne pole o velkosti end

# funkciu vykonavaju pracovne vlakna, kde pracuju s vlaknom shared
# po dokonceni maju byt vo vsetkych prvkoch pola 1tky
def work(shared):
    while True:
        # skontroluje ci shared.counter nie je mimo velkosti pola
        if shared.counter >= shared.end:
            return

        # zvysi hodnotu prvku pola na indexe shared.counter
        shared.elms[shared.counter] += 1

        # zvysi hodnotu pocitadla shared.counter
        shared.counter += 1

# program...
def main():
    sh = Shared(1_000_000)    # zdielany objekt o velkosti 1 000 000

    # identifikator ulozeny v t1
    # 1. argument - funkcia ktoru ma vlakno vykonavat
    # dalsie argumenty - su argumenty funkcie, ktora je v prvom argumente
    t1 = Thread(work, sh)           # 1. pracovne vlakno
    t2 = Thread(work, sh)           # 2. pracovne vlakno

    # pockat na dokoncenie prace oboch vlaken
    t1.join()
    t2.join()

    # spocitat vyskyty hodnot a vypisat ich na obrazovku
    values = [[x,sh.elms.count(x)] for x in set(sh.elms)]
    print(values)
    # pozn. Ako dosledok porusenia integrity dat Shell vypisuje spravu
    # IndexError: list index out of range
        
if __name__== "__main__":
  main()
