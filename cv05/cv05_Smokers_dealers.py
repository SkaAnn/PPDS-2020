from fei.ppds import *
from time import sleep
from random import randint

class Shared(object):
    def __init__(self):
        self.mutex = Mutex()
        self.agentSem = Semaphore(1)
        
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)
 
        self.isTobacco = False
        self.isMatch = False
        self.isPaper = False
        
        self.tobaccoSem = Semaphore(0)
        self.paperSem = Semaphore(0)
        self.matchSem = Semaphore(0)

def make_cigarette():
    sleep(randint(0,10)/100)

def smoke():
    sleep(randint(0,10)/100)

# fajciar s nekonecnym mnozstvom zapaliek
def smoker_match(shared):
    while True:
        #sleep(randint(0,10)/100)
        print("SM caka na suroviny")
        shared.matchSem.wait()
        print("SM dostal suroviny")
        make_cigarette()
        shared.agentSem.signal()
        smoke()
        print("SM vyfajcil cigaretu")

        
# fajciar s nekonecnym mnozstvom tabaku
def smoker_tobacco(shared):
    while True:
        #sleep(randint(0,10)/100)
        print("ST caka na suroviny")
        shared.tobaccoSem.wait()
        print("ST dostal suroviny")
        make_cigarette()
        shared.agentSem.signal()
        smoke()
        print("ST vyfajcil cigaretu")


# fajciar s nekonecnym mnozstvom papiera
def smoker_paper(shared):
    while True:
        #sleep(randint(0,10)/100)
        print("SP caka na suroviny")
        shared.paperSem.wait()
        print("SP dostal suroviny")
        make_cigarette()
        shared.agentSem.signal()
        smoke()
        print("SP vyfajcil cigaretu")

# agent distribuuje tabak a papier
def agent_1(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()
        
# agent distribuuje papier a zapalky
def agent_2(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.agentSem.wait()
        print("agent: paper, match")
        shared.paper.signal()
        shared.match.signal()

# agent distribuuje tabak a zapalky
def agent_3(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.agentSem.wait()
        print("agent: tobacco, match")
        shared.tobacco.signal()
        shared.match.signal()

# dealer distribuuje papier
def dealer_paper(shared):
    while True:
        shared.paper.wait()
        print("Dealer PAPIERA zobudeny")
        print(shared.isPaper, shared.isTobacco, shared.isMatch)
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco = False
            shared.matchSem.signal()
        elif shared.isMatch:
            shared.isMatch = False
            shared.tobaccoSem.signal()
        else:
            shared.isPaper = True
        shared.mutex.unlock()
        print(shared.isPaper, shared.isTobacco, shared.isMatch)
        

# dealer distribuuje tabak
def dealer_tobacco(shared):
    while True:
        shared.tobacco.wait()
        print("Dealer TABAKU zobudeny")
        print(shared.isPaper, shared.isTobacco, shared.isMatch)
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper = False
            shared.matchSem.signal()
        elif shared.isMatch:
            shared.isMatch = False
            shared.paperSem.signal()
        else:
            shared.isTobacco = True
        shared.mutex.unlock()
        print(shared.isPaper, shared.isTobacco, shared.isMatch)

# dealer distribuuje zapalky
def dealer_match(shared):
    while True:
        shared.match.wait()
        print("Dealer ZAPALIEK zobudeny")
        print(shared.isPaper, shared.isTobacco, shared.isMatch)
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper = False
            shared.tobaccoSem.signal()
        elif shared.isTobacco:
            shared.isTobacco = False
            shared.paperSem.signal()
        else:
            shared.isMatch = True
        shared.mutex.unlock()
        print(shared.isPaper, shared.isTobacco, shared.isMatch)

def run_model():
    shared = Shared()

    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    dealers = []
    dealers.append(Thread(dealer_match, shared))
    dealers.append(Thread(dealer_tobacco, shared))
    dealers.append(Thread(dealer_paper, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in agents + smokers + dealers:
        t.join()
    
if __name__ == "__main__":
    run_model()
