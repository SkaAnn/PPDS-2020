# nacitame modul 'ppds', v ktorom mame definovanu triedu 'Thread'
from ppds import *
#from ppds import Mutex, Thread

# definicia triedy 'Shared'
class Shared():
    def __init__(self, arr_size):
        self.counter = 0
        self.end = arr_size
        self.elms = [0] * self.end
        ## vytvor mutex - zamok
        self.mutex = Mutex()

## mutex zablokuje cinnost vlakna pomocou mutex.lock() az do odvolania prikazom mutex.unlock()
# definicia funkcie vlakna
def fnc_test(shared):
    while True:
        if (shared.counter > (shared.end - 1)):
            return
        else:
            shared.mutex.lock()
            shared.elms[shared.counter] += 1
            shared.counter += 1 
            shared.mutex.unlock()
 
# vytvorenie instancie triedy 'Shared'
shared = Shared(1_000_000)


# do 't1' ulozime identifikator pracovneho vlakna
# prvy argument pri vytvarani objektu typu 'Thread' je funkcia, ktoru ma
# vlakno vykonavat
# dalsie argumenty sa predaju funkcii, ktora je definovana prvym argumentom
t1 = Thread(fnc_test, shared)

t2 = Thread(fnc_test, shared)
 
# pockame na dokoncenie behu vlakna
t1.join()
t2.join()

## spocitajte vyskyty hodnot a vypiste ich na obrazovku
values = [[x,shared.elms.count(x)] for x in set(shared.elms)]
print(values)
