import time
import random
try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui
import eventhandlers as e
import globals
import helpers

class player():
    def __init__(self, role, startx, starty, color):
        self.role = role
        self.x, self.y = startx, starty
        self.color = color
        self.direction = 'right'
        self.nose_x, self.nose_y = self.x + 1, self.y
        self.carrying_inventory = 0
        self.carrying_box = False
        #speed is measured in grid squares per screen refresh.
        #For example, 1.0/15 means it takes 15 draws to move one 
        #grid square
        self.speed = globals.player_default_speed

        #self.moving = False
        self.target_x = self.x
        self.target_y = self.y

    def move_up(self):
        if not self.moving:
            self.direction = 'up'
            if (self.x, self.y - 1) not in globals.blocked_coordinates: 
                self.old_y, self.target_y = self.y, int(self.y - 1)
                self.moving = True

    def move_down(self):
        if not self.moving:
            self.direction = 'down'
            if (self.x, self.y + 1) not in globals.blocked_coordinates: 
                self.old_y, self.target_y = self.y, int(self.y + 1)
                self.moving = True

    def move_right(self):
        if not self.moving:
            self.direction = 'right'
            if (self.x + 1, self.y) not in globals.blocked_coordinates: 
                self.old_x, self.target_x = self.x, int(self.x + 1)
                self.moving = True

    def move_left(self):
        if not self.moving:
            self.direction = 'left'
            if (self.x - 1, self.y) not in globals.blocked_coordinates: 
                self.old_x, self.target_x = self.x, int(self.x - 1)
                self.direction = 'left'
                self.moving = True
                self.direction = 'left'

    def set_nose(self):
        nose_offset = {'up': (0, -1), 'down': (0,1), 'right': (1, 0), 'left': (-1, 0)}
        (self.nose_x, self.nose_y) = (self.x + nose_offset[self.direction][0], self.y + nose_offset[self.direction][1])

    def pick_up_box(self):
        assert self.role == 'packer', 'Only the packer can pick up box.'
        if not self.carrying_box:
            current_totes = globals.totes
            for box in current_totes:
                if box.home == 'divert' and ((int(round(box.x)), int(round(box.y))) == (self.x, self.y)\
                            or (int(round(box.x)), int(round(box.y))) == (self.nose_x, self.nose_y)):
                    box.being_carried = True
                    box.home = 'player'
                    self.carrying_box = box
                    return

    def pack_shipment(self):
        assert self.role == 'picker', "Must be picker to call pack_shipment"
        if self.carrying_inventory > 0 and globals.order:
            for dropoff_point in globals.dropoff_points:
                if ((dropoff_point.x, dropoff_point.y) == (int(self.nose_x), int(self.nose_y))):
                    print 'Packing a shipment worth', self.carrying_inventory, 'points'
                    globals.score += self.carrying_inventory
                    self.carrying_inventory = 0
                    if not helpers.check_open_order():
                        globals.order = False
                    return

    def shelve_box(self):
        assert self.carrying_box, "Must be carrying box to call shelve_box"
        assert self.role == 'packer', "Must be packer to call shelve_box"
        for bay in globals.bays:
            if not bay.full:
                if (int(self.carrying_box.x), int(self.carrying_box.y)) == (bay.x, bay.y):
                    self.carrying_box.x, self.carrying_box.y = bay.x, bay.y
                    bay.full = self.carrying_box
                    bay.full.home = 'shelf'
                    self.carrying_box.shelved = True
                    self.carrying_box = False
                    return

    def pick_inventory(self):
        assert self.role == 'picker', "You must be picker to call pick_item"
        for bay in globals.bays:
            if bay.full and bay.full.on_order > 0:
                if ((bay.x, bay.y) == (int(self.nose_x), int(self.nose_y))):
                    tote = bay.full
                    print 'picking inventory'
                    tote.inventory -= 1
                    tote.on_order -= 1
                    self.carrying_inventory += 1
                    if tote.inventory == 0:
                        bay.full = False
                        tote.shelved = False
                        globals.totes.remove(tote)
                        print globals.pickable_inventory
                        while tote in globals.pickable_inventory:
                            print globals.pickable_inventory
                            print 'removing tote from globals pickable inventory'
                            globals.pickable_inventory.remove(tote)
                            time.sleep(1)

    def update_position(self):
        if self.x < self.target_x-.1: self.x += self.speed
        elif self.x > self.target_x+.1: self.x -= self.speed
        elif self.y < self.target_y-.1: self.y += self.speed
        elif self.y > self.target_y+.1: self.y -= self.speed
        else:
            self.x, self.y = self.target_x, self.target_y
            self.set_nose()
            self.moving = False
            if self.role == 'packer': 
                self.pick_up_box()
            else:
                self.pick_inventory()
                self.pack_shipment()
        if self.carrying_box:
            if self.direction == 'up': self.carrying_box.x, self.carrying_box.y = self.x, self.y - 1
            if self.direction == 'right': self.carrying_box.x, self.carrying_box.y = self.x + 1, self.y
            if self.direction == 'down': self.carrying_box.x, self.carrying_box.y = self.x, self.y + 1
            if self.direction == 'left': self.carrying_box.x, self.carrying_box.y = self.x - 1, self.y
            self.shelve_box()

    def draw(self, canvas):
        self.update_position()
        g = globals.grid_size
        canvas.draw_circle([g*self.x, g*self.y], g/2, 1, 'black', self.color)
        nose_line = {'right': ([g*self.x, g*self.y], [g*self.x+g, g*self.y]),
                'left': ([g*self.x, g*self.y], [g*self.x-g, g*self.y]),
                'up': ([g*self.x, g*self.y], [g*self.x, g*self.y-g]),
                'down': ([g*self.x, g*self.y], [g*self.x, g*self.y+g])}
        canvas.draw_line(nose_line[self.direction][0], nose_line[self.direction][1], 5, self.color)

class dropoff_point():
    def __init__(self, x, y):
        self.x, self.y = x, y
        globals.blocked_coordinates.add((x,y))
    
    def draw(self, canvas):
        g = globals.grid_size
        canvas.draw_polygon([(g*self.x - g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y + g/2),
                             (g*self.x - g/2, g*self.y + g/2)],
                          1, 'blue', 'yellow')

class tote():
    def __init__(self, x, y, inventory, divert=False):
        self.x, self.y = x, y
        self.inventory = inventory
        
        self.on_order = 0
        self.collected = False
        self.being_carried = False
        self.shelved = False
        self.main_conveyor = True
        self.divert = divert
        self.speed = globals.default_conveyor_speed
        self.home = 'conveyor'

    def make_pickable(self):
        for i in range(0, self.inventory):
            globals.pickable_inventory.append(self)

    def draw(self, canvas):
            g = globals.grid_size
            if not self.divert:
                self.x -= self.speed

            else:
                if self.home == 'conveyor':
                    if self.x > globals.divert_x:
                        self.x -= self.speed
                    else:
                        self.x = globals.divert_x
                        self.home = 'turnoff'

                if self.home == 'turnoff':
                    if self.y > globals.divert_y:
                        self.y -= globals.divert_speed
                    else:
                        self.y = globals.divert_y
                        self.home = 'divert'

                if self.home == 'divert':
                    self.make_pickable()
                    if self.x < globals.divert_end_x:
                        self.x += globals.divert_speed
                    else:
                        self.x = globals.divert_end_x
                    
            color = {False: 'white', True: 'orange'}
            canvas.draw_polygon([(g*self.x - g/2, g*self.y - g/2),
                                 (g*self.x + g/2, g*self.y - g/2),
                                 (g*self.x + g/2, g*self.y + g/2),
                                 (g*self.x - g/2, g*self.y + g/2)],
                    1, 'blue', color[self.on_order > 0])

            width = globals.frame.get_canvas_textwidth(str(self.inventory), globals.tote_font_size)
            canvas.draw_text(str(self.inventory), [g*self.x - .5*width, g*self.y + .4*g], globals.tote_font_size, 'blue')

class barrier():
    def __init__(self, x, y):
        self.x, self.y = x, y
        globals.blocked_coordinates.add((x,y))

    def draw(self, canvas):
        g = globals.grid_size
        canvas.draw_polygon([(g*self.x - g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y + g/2),
                             (g*self.x - g/2, g*self.y + g/2)],
                                 1, 'black', 'green')

class bay():
    def __init__(self, x, y):
        self.x, self.y = x, y
        globals.blocked_coordinates.add((x, y))
        self.full = False
        self.needs_picked = True

    def draw(self, canvas):
        g = globals.grid_size
        canvas.draw_polygon([(g*self.x - g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y + g/2),
                             (g*self.x - g/2, g*self.y + g/2)],
                1, 'blue', 'teal')
  
class order():
    def __init__(self):
        self.time_remaining = 20
        max_order_items = min(globals.maximum_order, len(globals.pickable_inventory))
        try:
            self.order_size = random.randrange(1, max_order_items)
            random.shuffle(globals.pickable_inventory)
            print 'Creating order for', self.order_size, 'items' 
            for i in range(0, self.order_size):
                tote = globals.pickable_inventory[i]
                tote.on_order += 1
            globals.order_ready_to_pick = True
            globals.order = self

        except:
            print 'Could not build order. No pickable inventory'

    def draw(self, canvas):
       g = globals.grid_size
       canvas.draw_text('Order Up Qty: ' + str(self.order_size) + ' Time: ' + str(self.time_remaining), [10, 8*g], 14, 'blue')
