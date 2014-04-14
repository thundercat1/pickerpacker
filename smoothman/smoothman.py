import random
from classes import*
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

globals.p = player()
print globals.p

for i in range(0,10):
    x = random.randrange(1, globals.board_size[0])
    y = random.randrange(1, globals.board_size[1])
    points = random.randint(1,5)*5
    globals.targets.add(target(x, y, points))

for i in range(0,2):
    x = random.randrange(1, globals.board_size[0])
    y = random.randrange(1, globals.board_size[1])
    globals.dropoff_points.add(dropoff_point(x,y))

globals.barriers.add(barrier((15, 10), (17, 10), (17, 15), (15, 15)))

#for target in targets:
#    #TODO set changes size during iteration, may actually fail if a target gets built on top of blocked coordinate
#    if (target.x, target.y) in blocked_coordinates: targets.remove(target)

print 'Frame about to start. p =', globals.p
frame.start()
