import random
import copy
import globals

def event_happens(p):
    #Takes p from 0 to 100 and decides whether or not it happened
    r = random.randrange(1,100)
    return p > r


def clean_up_totes():
    current_totes = copy.copy(globals.totes)
    for tote in current_totes:
        if tote.x < 0:
            globals.totes.remove(tote)
