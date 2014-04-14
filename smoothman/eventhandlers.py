import random
from classes import*
try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui

import globals

print globals.p

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
        if key == 'right': globals.p.move_right()
        if key == 'down': globals.p.move_down()
        if key == 'left': globals.p.move_left()
        if key == 'up': globals.p.move_up()
    except: print 'Invalid key press. Need to use arrow keys'
    

