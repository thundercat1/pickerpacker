import random
import copy
import classes
import globals

def event_happens(p):
    #Takes p from 0 to 1 and decides whether or not it happened
    r = random.randrange(1,100)
    return p*100 > r


def clean_up_totes():
    current_totes = copy.copy(globals.totes)
    for tote in current_totes:
        if tote.x < -5:
            globals.totes.remove(tote)

def place_order():
    order = classes.order()

def check_open_order():
    for tote in globals.totes:
        if tote.on_order > 0:
            return True
    return False

def pause_game():
    for timer in globals.timers:
        timer.stop()

def start_timers():
    for timer in globals.timers:
        timer.start()

def get_current_instruction():
#{'move': False, 'divert': False, 'pack': False, 'order': False, 'pick': False, 'ship': False, 'playing': False, 'gameover': False   }
    for step in globals.progress_steps:
        if not globals.progress_completed[step]:
            return globals.instructions[step]

