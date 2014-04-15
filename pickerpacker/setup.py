import random
try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui

import eventhandlers as e
import globals
import classes
import helpers


def go():
    with open('floorplan.txt','r') as f:
        for line in f:
            args = line.strip().split(',')
            if args[0] == 'width':
                globals.board_size[0] = int(args[1])
            elif args[0] == 'height':
                globals.board_size[1] = int(args[1])
            elif args[0] == 'bay':
                globals.bays.add(classes.bay(int(args[1]), int(args[2])))
            elif args[0] == 'barrier':
                globals.barriers.add(classes.barrier(int(args[1]), int(args[2])))
            elif args[0] == 'dropoff_point':
                globals.dropoff_points.add(classes.dropoff_point(int(args[1]), int(args[2])))
            elif args[0] == 'tote':
                globals.totes.add(classes.tote(int(args[1]), int(args[2]), random.randint(1,10)))
    
    globals.frame = simplegui.create_frame('Warehouse Man', globals.grid_size * globals.board_size[0], globals.grid_size * globals.board_size[1])
    globals.frame.set_canvas_background('white')
    globals.frame.set_draw_handler(e.draw_handler)
    globals.frame.set_keydown_handler(e.keydown_handler)
    globals.frame.set_keyup_handler(e.keyup_handler)
    
    cadence = simplegui.create_timer(100, e.poll_keyboard)
    cadence.start()
    tote_generator_timer = simplegui.create_timer(globals.tote_spawn_delay, e.generate_tote)
    tote_generator_timer.start()
    cleanup_timer = simplegui.create_timer(1000, helpers.clean_up_totes)
    cleanup_timer.start()

    globals.packer = classes.player('packer', 13, 8, 'blue')
    globals.picker = classes.player('picker', 2, 8, 'cyan')
    globals.active_player = globals.packer
    globals.inactive_player = globals.picker
    
    globals.frame.start()
    
    #for i in range(0,10):
    #    x = random.randrange(1, globals.board_size[0])
    #    y = random.randrange(1, globals.board_size[1])
    #    points = random.randint(1,5)*5
    #    globals.totes.add(classes.tote(x, y, points))
    #
    #for i in range(0,2):
    #    x = random.randrange(1, globals.board_size[0])
    #    y = random.randrange(1, globals.board_size[1])
    #    globals.dropoff_points.add(classes.dropoff_point(x,y))
    
    #globals.barriers.add(classes.barrier((15, 10), (17, 10), (17, 15), (15, 15)))
    
    #for i in range(0,2):
    #    x = random.randrange(1, globals.board_size[0])
    #    y = random.randrange(1, globals.board_size[1])
    #    globals.bays.add(classes.bay(x,y))
    #
    #illegal_totes = set([])
    #for tote in globals.totes:
    #    if (tote.x, tote.y) in globals.blocked_coordinates:
    #        illegal_totes.add(tote)
    #
    #for illegal_tote in illegal_totes:
