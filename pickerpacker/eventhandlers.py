import random
import classes
import copy
import helpers
try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui

import globals

def draw_handler(canvas):
    globals.packer.draw(canvas)
    globals.picker.draw(canvas)
    for bay in globals.bays:
        bay.draw(canvas)
    for dropoff_point in globals.dropoff_points:
        dropoff_point.draw(canvas)
    for barrier in globals.barriers:
        barrier.draw(canvas)

    if globals.order:
        globals.order.draw(canvas)

    #TODO: Copy.copy won't work in codeskulptor, so need to find another solution
    current_totes = copy.copy(globals.totes)
    for tote in current_totes:
        tote.draw(canvas)
    canvas.draw_text(str(globals.score), [globals.grid_size * (globals.board_size[0]-2), globals.grid_size * (globals.board_size[1])], 30, 'blue')
    canvas.draw_text('You are ' + str(globals.active_player.role) + '. Change with spacebar', [1*globals.grid_size, 13*globals.grid_size], 12, 'blue')

    if not globals.has_moved:
        instruction = 'Blue player is packer. He gets tote and stores it in a teal bay'
        instruction2 = 'Cyan player is picker, who collects from full bays to yellow pack station'
        instruction3 = 'Arrow keys move players. Space bar switches to other player'
        canvas.draw_text(instruction, [5, 100], 12, 'blue')
        canvas.draw_text(instruction2, [5, 120], 12, 'blue')
        canvas.draw_text(instruction3, [5, 140], 12, 'blue')

    if globals.game_over:
        canvas.draw_text('You Lose! Close the window and restart to play again', [20, 100], 18, 'blue')
    
def keydown_handler(keycode):
    globals.has_moved = True
    key = ''
    try:
        key = globals.keys[keycode]
    except: print 'Invalid key press. Need to use arrow keys'
    if key == 'right': globals.right = True
    if key == 'down': globals.down = True
    if key == 'left': globals.left = True
    if key == 'up': globals.up = True
    if key == 'space': globals.active_player, globals.inactive_player = globals.inactive_player, globals.active_player
    
def keyup_handler(keycode):
    key = ''
    try:
        key = globals.keys[keycode]
    except: print 'Invalid key press. Need to use arrow keys'
    if key == 'right': globals.right = False
    if key == 'down': globals.down = False
    if key == 'left': globals.left = False
    if key == 'up': globals.up = False

def poll_keyboard():
    if globals.right: globals.active_player.move_right()
    elif globals.left: globals.active_player.move_left()

    if globals.up: globals.active_player.move_up()
    elif globals.down: globals.active_player.move_down()

def generate_tote():
    if len(globals.totes) < 35:
        divert =  helpers.event_happens(globals.divert_odds)
        globals.totes.append(classes.tote(20, 11, random.randint(1,globals.max_tote_size), divert))

def age_orders():
    if globals.order:
        if globals.order.time_remaining == 0:
            helpers.end_game()
        else:
            globals.order.time_remaining -= 1
