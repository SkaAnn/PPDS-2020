# sl 43
# iterator je kazdy objekt, ktory ma implementovane metody __iter__ a __next__

class MyIterator():
    def __init__(self, xs):
        self.xs = xs    # zoznam prvkov postupnosti, cez ktory budeme iterovat

    # vrati iterovatelny objekt
    def __iter__(self):
        return self

    # funkcia ktora postupne vrati (iteruje) prvky vstupu xs
    def __next__(self):
        if self.xs:
            return self.xs.pop(0)
        # vyminka pri vyberani prvku z prazdneho zoznamu
        else:
            raise StopIteration
def main():
    mI = MyIterator([0, 1, 2])
    # for zavola automaticky metodu __next__ objektu iteratora, ktory ziska cez __iter__
    for i in mI:
        print(i)

    # next(mI) # zavolanie vyhodi vynimku StopIteration

if __name__ == "__main__":
    main()
        
        
