#!/usr/bin/env python3

from fei.ppds import Thread, Mutex, Semaphore, Event, print
from time import sleep
from random import randint, shuffle

class Shared(object):
    def __init__(self, resources, smokers):
        self.agentSem = Semaphore(1)
        
        self.res = {resources[i]:{
            'sem':Semaphore(0),
            'val':0,
            }
                    for i in range(len(resources))}
        self.res['mutex'] = Mutex()

        self.smo = {k:{
            'sem':Semaphore(0),
            'need':v,
            }
                    for k,v in smokers.items()}

def make_cigarette(who):
    print("*** makes cigarette: %s" % who)
    sleep(randint(0,10)/100)

def smoke(who):
    #print("\tsmokes: %s" % who)
    sleep(randint(0,10)/100)

def smoker(smoker_id, shared):
    while True:
        sleep(randint(0,10)/100)
        shared.smo[smoker_id]['sem'].wait()
        make_cigarette("smoker %s" % smoker_id)
        shared.agentSem.signal()
        smoke("smoker %s" % smoker_id)

def agent(agent_id, res, shared):
    while True:
        #sleep(randint(0,1)/100)
        sleep(randint(9,10)/100)
        shared.agentSem.wait()
        shuffle(res)
        print("agent %s:" % agent_id, res)
        for r in res:
            shared.res[r]['sem'].signal()

def copy_res(old):
    new = {k:dict() for k in old.keys()}
    for k in old.keys():
        if k == 'mutex':
            continue
        new[k]['val'] = old[k]['val']
    return new

def print_res(res_id, old, new):
    s = "\tp_w_%s: " % res_id
    for k in old.keys():
        if k == 'mutex':
            continue
        s += "%s %d-->%d; " % (k, old[k]['val'], new[k]['val'])
    print(s)

def check_smokers_res(res_avail, shared):
    smo_avail = []
    for s in shared.smo.keys():
        s_keys = shared.smo[s]['need'].keys()
        if not set(res_avail).issuperset(set(s_keys)):
            continue
        for need in s_keys:
            if shared.res[need]['val'] < shared.smo[s]['need'][need]:
                continue
        smo_avail.append(s)
    print("\tSMO_AVAIL=", smo_avail)
    return smo_avail
    
def pusher(res, shared):
    res_keys = list(shared.res.keys())
    while True:
        # diler caka na surovinu 'res'
        shared.res[res]['sem'].wait()

        # ked ju agent doda
        shared.res['mutex'].lock()
        # pre ucely vypisu stavu systemu pred zmenou
        tmpRes = copy_res(shared.res)

        # diler zvysi mnozstvo suroviny, ktoru dodava
        shared.res[res]['val'] += 1
        # zistime, ktore suroviny su k dispozicii na stole
        res_available = [k for k in shared.res.keys() if
             k != 'mutex' and shared.res[k]['val']]

        # ak nejake suroviny su k dispozicii
        # (nas diler pridal jednu surovinu, takze vzdy je tu
        # aspon 1 surovina k dispozicii),
        # zistime, ktore dostupne suroviny ktoremu fajciarovi
        # vyhovuju na zapalenie cigaretkY
        smo_available = check_smokers_res(res_available, shared)
        # nahodne vyberieme jedneho fajciara, ktory
        # moze fajcit. vsetci kandidati su v 'smo_available'
        # ak je tam iba jeden, je zrejme, ze ten bude
        # vybrany
        if smo_available:
            smoker = smo_available[randint(0, len(smo_available)-1)]
            shared.smo[smoker]['sem'].signal()
            # musime odobrat ingrediencie k fajceniu
            # otazka: nemal by tak cinit fajciar vo funkci
            # make_cigarette?!
            for r in shared.smo[smoker]['need'].keys():
                shared.res[r]['val'] -= shared.smo[smoker]['need'][r]

        #print_res(res, tmpRes, shared.res)
        shared.res['mutex'].unlock()        

def run_model():
    # oznacenie zdrojov
    RES_T = 'T'
    RES_P = 'P'
    RES_M = 'M'
    RES_L = 'L'
    resources = [RES_L, RES_T, RES_P, RES_M]
    
    # konfiguracia agenta, slovnik
    #   id_agenta: zoznam zdrojov, ktore generuje
    #   id_agenta moze byt lubovolny retazec
    #   zdroj musi byt zo zoznamu 'resources'
    agents = {
        RES_T+RES_P: [RES_T, RES_P],
        RES_P+RES_M: [RES_P, RES_M],
        RES_M+RES_T: [RES_M, RES_T],
        #RES_L: [RES_L],
        }
    
    # konfiguracia fajciarov, slovnik
    #   id_fajciara: zoznam zdrojov, ktore potrebuje
    #                ziskat od agenta
    #   id_fajciara moze byt lubovolny retazec
    #   zoznam zdrojov je slovnik obsahujuci id zdroja a pocet;
    #       pocet vyjadruje, kolko kusov zdroja potrebuje fajciar
    #       na urobenie cigarety
    #   id zdroja musi byt zo zoznamu 'resources'
    smokers = {
        RES_T : {RES_M:1, RES_P:1},
        RES_P : {RES_M:1, RES_T:1},
        RES_M : {RES_T:1, RES_P:1},
        #RES_T+RES_P : {RES_M:1},
        }
    
    pushers_t = []
    agents_t = []
    smokers_t = []

    shared = Shared(resources, smokers)

    # vytvorime tolko dilerov, kolko je zdrojov;
    # kazdy diler bude spracovavat prave jeden zdroj od agenta
    for i in range(len(resources)):
        pushers_t.append(Thread(pusher, resources[i], shared))

    # kazdy agent ma svoje id, zoznam zdrojov, ktore generuje,
    # a pristup ku modelu zdrojov systemu
    for a in agents.keys():
        agents_t.append(Thread(agent, a, agents[a], shared))

    # kazdy fajciar ma svoje id a pristup k modelu zdrojov
    for s in smokers.keys():
        smokers_t.append(Thread(smoker, s, shared))

    # cakanie na ukoncenie behu vlakien
    for t in agents_t + smokers_t + pushers_t:
        t.join()
    
if __name__ == "__main__":
    run_model()
