import random

def event_happens(p):
    #Takes p from 0 to 100 and decides whether or not it happened
    r = random.randrange(1,100)
    return p > r
