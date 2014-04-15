import random
from classes import*
try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui

import globals

def draw_handler(canvas):
    globals.p.draw(canvas)

    for target in globals.targets:
        target.draw(canvas)
    for dropoff_point in globals.dropoff_points:
        dropoff_point.draw(canvas)
    for barrier in globals.barriers:
        barrier.draw(canvas)
    canvas.draw_text(str(globals.p.score), [globals.grid_size * (globals.board_size[0]-3), globals.grid_size * (globals.board_size[1]-2)], 30, 'blue')

    if not globals.has_moved:
        canvas.draw_text('Collect the boxes and carry them to the yellow dropoff points. Avoid the green barriers.', [20, 100], 16, 'blue')

    if globals.win:
        canvas.draw_text('You win! Close the window and restart to play again', [20, 100], 18, 'blue')
    
def keydown_handler(keycode):
    globals.has_moved = True
    try:
        key = globals.keys[keycode]
    except: print 'Invalid key press. Need to use arrow keys'
    if key == 'right': 
        globals.right = True
    if key == 'down': 
        globals.down = True
    if key == 'left': 
        globals.left = True
    if key == 'up': 
        globals.up = True
    
def keyup_handler(keycode):
    #try:
    key = globals.keys[keycode]
    if key == 'right': globals.right = False
    if key == 'down': globals.down = False
    if key == 'left': globals.left = False
    if key == 'up': globals.up = False
    #except: print 'Invalid key press. Need to use arrow keys'

def poll_keyboard():
    if globals.right: globals.p.move_right()
    elif globals.left: globals.p.move_left()

    if globals.up: globals.p.move_up()
    elif globals.down: globals.p.move_down()
