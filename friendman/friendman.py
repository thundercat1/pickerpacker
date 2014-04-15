import random
import classes
try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui

import eventhandlers as e
import globals

frame = simplegui.create_frame('Walking Player', globals.grid_size * globals.board_size[0], globals.grid_size * globals.board_size[1])
frame.set_canvas_background('white')
frame.set_draw_handler(e.draw_handler)
frame.set_keydown_handler(e.keydown_handler)
frame.set_keyup_handler(e.keyup_handler)

cadence = simplegui.create_timer(100, e.poll_keyboard)
cadence.start()
globals.packer = classes.player('packer', 5, 5, 'blue')
globals.picker = classes.player('picker', 5, 20, 'cyan')
globals.active_player = globals.packer
globals.inactive_player = globals.picker

for i in range(0,10):
    x = random.randrange(1, globals.board_size[0])
    y = random.randrange(1, globals.board_size[1])
    points = random.randint(1,5)*5
    globals.totes.add(classes.tote(x, y, points))

for i in range(0,2):
    x = random.randrange(1, globals.board_size[0])
    y = random.randrange(1, globals.board_size[1])
    globals.dropoff_points.add(classes.dropoff_point(x,y))

#globals.barriers.add(classes.barrier((15, 10), (17, 10), (17, 15), (15, 15)))

for i in range(0,2):
    x = random.randrange(1, globals.board_size[0])
    y = random.randrange(1, globals.board_size[1])
    globals.bays.add(classes.bay(x,y))

illegal_totes = set([])
for tote in globals.totes:
    if (tote.x, tote.y) in globals.blocked_coordinates:
        illegal_totes.add(tote)

for illegal_tote in illegal_totes:
    globals.totes.remove(illegal_tote)

frame.start()
