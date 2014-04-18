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
    canvas.draw_text(str(globals.score) + 'pts', [globals.grid_size * (globals.board_size[0]-4), globals.grid_size * (globals.board_size[1])], 28, 'blue')
    canvas.draw_text('Controlling: ' + globals.active_player.role, [10, globals.grid_size], 14, 'blue')
    canvas.draw_text(helpers.get_current_instruction(), [10, 7.5*globals.grid_size], 12, 'blue')

    if globals.game_over:
        canvas.draw_text('You Lose! Close the window and restart to play again', [20, 100], 18, 'blue')
    
def keydown_handler(keycode):
    key = ''
    try:
        key = globals.keys[keycode]
    except: print 'Invalid key press. Need to use arrow keys'
    globals.progress_completed['move'] = True
    if key == 'right': globals.right = True
    if key == 'down': globals.down = True
    if key == 'left': globals.left = True
    if key == 'up': globals.up = True
    if key == 'space': 
        globals.active_player, globals.inactive_player = globals.inactive_player, globals.active_player
        globals.progress_completed['change_player'] = True
    
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
            globals.game_over = True
            globals.progress_completed['play_game'] = True
            helpers.pause_game()
        else:
            globals.order.time_remaining -= 1
