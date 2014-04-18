import random
import copy
import classes
import globals

def event_happens(p):
    #Takes p from 0 to 100 and decides whether or not it happened
    r = random.randrange(1,100)
    return p > r


def clean_up_totes():
    current_totes = copy.copy(globals.totes)
    for tote in current_totes:
        if tote.x < -5:
            globals.totes.remove(tote)

def place_order():
    order = classes.order()

def check_open_order():
    print 'Checking to see whether items need picking'
    for tote in globals.totes:
        if tote.on_order > 0:
            print 'Totes still need picking'
            return True
    print 'No totes to pick'
    return False

