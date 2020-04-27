# pseudokod sl 55
# generator je VOLATELNY objekt=FUNKCIA, ktory vrati ciastkove vysledky vypoctu pomocou yield
def mygenerator(n):
    while n:
        n -= 1
        yield n

def mygenerator2(n):
    # to co bude vykonavat fun __next__ v iteratore?
    i = 0
    while i<n:
        yield i
        i += 1

def in_cycle():
    # zavolanim funkcie generatora ziskam objekt generatora = iterator
    mG = mygenerator(3)
    print(mG)
    # preto funkciu generatora mozem pouzivat v cykle
    for i in mG:
        print(i)

def no_cycle():
    mG = mygenerator2(4)
    print(mG)
    # na aktivovanie generatoroveho iteratora a nasledne iterovanie pouzivam funkciu __next__
    print(next(mG))
    print(next(mG))
    print(next(mG))
    print(next(mG))
    # print(next(mG)) # vyvola vynimku StopIteration
    # vycerpany objekt generatora nie je mozne opat pouzit, treba vygenerovat novy

if __name__ == "__main__":
    in_cycle()  # generator pouzivany v cykly
    no_cycle()  # generator pouzivany bez cyklu
        
