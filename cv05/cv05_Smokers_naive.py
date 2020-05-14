from fei.ppds import *
from time import sleep
from random import randint

class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.agentSem = Semaphore(1)

def make_cigarette():
    sleep(randint(0,10)/100)

def smoke():
    sleep(randint(0,10)/100)

# fajciar s nekonecnym mnozstvom zapaliek
def smoker_match(shared):
    while True:
        sleep(randint(0,10)/100)
        print("SM caka na papier")
        shared.paper.wait()
        print("+SM dostal papier")
        print("SM caka na tabak")
        shared.tobacco.wait()
        print("+SM dostal tabak")
        make_cigarette()
        shared.agentSem.signal()
        smoke()
        print("SM vyfajcil cigaretu")

# fajciar s nekonecnym mnozstvom tabaku
def smoker_tobacco(shared):
    while True:
        sleep(randint(0,10)/100)
        print("ST caka na zapalky")
        shared.match.wait()
        print("+ST dostal zapalky")
        print("ST caka na papier")
        shared.paper.wait()        
        print("+ST dostal papier")
        make_cigarette()
        shared.agentSem.signal()
        smoke()
        print("ST vyfajcil cigaretu")

# fajciar s nekonecnym mnozstvom papiera
def smoker_paper(shared):
    while True:
        sleep(randint(0,10)/100)
        print("SP caka na tabak")
        shared.tobacco.wait()
        print("+SP dostal tabak")
        print("SP caka na zapalky")
        shared.match.wait()
        print("+SP dostal zapalky")
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

def run_model():
    shared = Shared()

    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in agents + smokers:
        t.join()
    
if __name__ == "__main__":
    run_model()
