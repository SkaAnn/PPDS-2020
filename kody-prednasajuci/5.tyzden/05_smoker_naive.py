#!/usr/bin/env python3

from fei.ppds import Thread, Mutex, Semaphore, Event, print
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

def smoker_match(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.paper.wait()
        print("\tpaper: tooken by smoker_match")
        shared.tobacco.wait()
        print("smokes: smoker_match")
        make_cigarette()
        shared.agentSem.signal()
        smoke()

def smoker_tobacco(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.match.wait()
        print("\tmatch: tooken by smoker_tobacco")
        shared.paper.wait()        
        print("smokes: smoker_tobacco")
        make_cigarette()
        shared.agentSem.signal()
        smoke()

def smoker_paper(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.tobacco.wait()
        print("\ttobacco: tooken by smoker_paper")
        shared.match.wait()
        print("smokes: smoker_paper")
        make_cigarette()
        shared.agentSem.signal()
        smoke()
    
def agent_1(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()

def agent_2(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.agentSem.wait()
        print("agent: paper, match")
        shared.paper.signal()
        shared.match.signal()

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
