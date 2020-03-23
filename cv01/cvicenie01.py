## pozn. OBJAVI SA "CHYBA OUT OF RANGE", KVOLI PORUSENEJ INTEGRITE DAT 

## 1. Importujte modul ppds.
# nacitame modul 'ppds', v ktorom mame definovanu triedu 'Thread'
from ppds import *
 
## python nevie zdielat jednoduche datove typy,
## tak to musime vyriesit pomocou triedy !
## 2. Definujte zdielany objekt (triedu!) Shared s atribútmi counter, end, elms 
# definicia triedy 'Shared'
class Shared():
    ## nastavenie atributov v inicializacnej triede funkcie
    def __init__(self, arr_size):
        ## spolocne pocitadlo counter
        self.counter = 0
        ## velkost pola end
        self.end = arr_size
        ## celociselne pole elms o velkosti end s vynulovanymi prvkami
        self.elms = [0] * self.end
        
## 3. Definujte funkciu, ktora prijima zdielany objekt shared.
## Budu ju vykonavat pracovne vlakna
# definicia funkcie vlakna
def fnc_test(shared):
    while True:
        ## kontroluje, ci shared.counter nie je mimo velkosti pola;
        ## ak ano, cyklus sa prerusi a funkcia skonci
        if (shared.counter > (shared.end - 1)):
            return
        else:
            ## zvys hodnotu prvku zdielaneho pola shared.elms na pozicii shared.counter
            shared.elms[shared.counter] += 1
            ## zvys hodnotu zdielaneho pocitadla shared.counter
            shared.counter += 1 
 
## 4. Definujte telo samotného vykonania programu:
## vytvorte zdieľaný objekt shared o veľkosti poľa napríklad 1 000 000
# vytvorenie instancie triedy 'Shared'
shared = Shared(1_000_000)


# do 't1' ulozime identifikator pracovneho vlakna
# prvy argument pri vytvarani objektu typu 'Thread' je funkcia, ktoru ma
# vlakno vykonavat
# dalsie argumenty sa predaju funkcii, ktora je definovana prvym argumentom
t1 = Thread(fnc_test, shared)

## vytvorte druhe pracovne vlakno a jeho identifikator ulozte
t2 = Thread(fnc_test, shared)
 
# pockame na dokoncenie behu vlakna
t1.join()
## pockame na dokoncenie behu 2. vlakna
t2.join()

## spocitajte vyskyty hodnot a vypiste ich na obrazovku
## https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
values = [[x,shared.elms.count(x)] for x in set(shared.elms)]
print(values)
