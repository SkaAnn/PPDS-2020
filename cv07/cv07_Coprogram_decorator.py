# pseudokod sl 96
# rozsirene generatory...
# vypise lubovolny pocet krat retazec "Oh no: I found substring in text"
# ak sa v nacitanom texte nachadza slovo, ktore je v argumente koprogramu

# aby sme nemuseli pri vytvoreni objektu koprogramu zakazdym volat next
# dekorator to vykona za nas, pri kazdom volani funkcie complain_about
# DEKORATOR
def coroutine(fn):
    def wrapper(*args, **kwargs):
        c = fn(*args, **kwargs)
        next(c)
        return c
    return wrapper

@coroutine  # pouzitie dekoratora
# koprogram = fun/metoda, v ktorej je slovo yield na pravej strane
def complain_about(substring):
    print("Please talk to me!")
    try:
        # pracuj az dokym nezavola close()
        while True:
            text = (yield)  # tu program caka na info, ktoru dostane zavolanim send()
            print(text)
            if substring in text:
                print("Oh no: I found a %s again!"%(substring))
    # zavolanie close() na koprogram vyhodi vynimku GeneratorExit
    except GeneratorExit:   # ak by nebola osetrena tak program len v tichosti skonci cinnost
        print("Ok, ok: I am quitting.")

# najlepsie sa skusa v idle prikazovom riadku
def main():
    coprog = complain_about("rano")
    print(coprog)
    # NEXT uz nemusim robit lebo to za mna spravi coroutine (ak ho trz dam, tak vyhlasi chybu)
    # next(coprog)

    coprog.send("Ranajky si dam o 8:00")
    coprog.send("rano mudrejsie vecer")
    coprog.send("Hranostaj je zviera")
    coprog.send("Slnko vyjde rano")
    coprog.close()
    # po ukonceni cinnosti koprogramu uz objekt nie je k dispozicii
    
if __name__ == "__main__":
    main()
