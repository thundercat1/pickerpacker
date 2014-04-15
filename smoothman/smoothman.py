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
globals.p = classes.player()

for i in range(0,10):
    x = random.randrange(1, globals.board_size[0])
    y = random.randrange(1, globals.board_size[1])
    points = random.randint(1,5)*5
    globals.targets.add(classes.target(x, y, points))

for i in range(0,2):
    x = random.randrange(1, globals.board_size[0])
    y = random.randrange(1, globals.board_size[1])
    globals.dropoff_points.add(classes.dropoff_point(x,y))

globals.barriers.add(classes.barrier((15, 10), (17, 10), (17, 15), (15, 15)))

illegal_targets = set([])
for target in globals.targets:
    if (target.x, target.y) in globals.blocked_coordinates:
        illegal_targets.add(target)

for illegal_target in illegal_targets:
    globals.targets.remove(illegal_target)

frame.start()
