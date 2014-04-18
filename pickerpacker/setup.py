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
                globals.totes.append(classes.tote(int(args[1]), int(args[2]), random.randint(1,10)))
    
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
    order_create_timer = simplegui.create_timer(globals.order_spawn_delay, helpers.place_order)
    order_create_timer.start()
    order_countdown_timer = simplegui.create_timer(1000, e.age_orders)
    order_countdown_timer.start()

    globals.packer = classes.player('packer', 13, 8, 'blue')
    globals.picker = classes.player('picker', 2, 8, 'cyan')
    globals.active_player = globals.packer
    globals.inactive_player = globals.picker
    
    globals.frame.start()
