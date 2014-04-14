import random
try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui
import eventhandlers as e
import globals

class player():
    def __init__(self):
        self.x, self.y = 0, 0
        self.direction = 'right'
        self.score = 0
        self.carrying_box = False

    def move_up(self):
        if (self.x, self.y - 1) not in globals.blocked_coordinates: self.y -= 1
        self.direction = 'up'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x, self.y - 1

    def move_down(self):
        if (self.x, self.y + 1) not in globals.blocked_coordinates: self.y += 1
        self.direction = 'down'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x, self.y + 1

    def move_right(self):
        if (self.x + 1, self.y) not in globals.blocked_coordinates: self.x += 1
        self.direction = 'right'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x + 1, self.y

    def move_left(self):
        if (self.x - 1, self.y) not in globals.blocked_coordinates: self.x -= 1
        self.direction = 'left'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x - 1, self.y

    def pick_up_box(self):
        if not self.carrying_box:
            for box in globals.targets:
                if box.x == self.x and box.y == self.y:
                    box.being_carried = True
                    self.carrying_box = box
                    print 'Player picked up a box'

    def did_i_score(self):
        if self.carrying_box:
            for dropoff_point in globals.dropoff_points:
                if self.carrying_box.x == dropoff_point.x and self.carrying_box.y == dropoff_point.y:
                    self.score += self.carrying_box.points
                    self.carrying_box.collected = True
                    self.carrying_box.being_carried = False
                    globals.targets.remove(self.carrying_box)
                    self.carrying_box = False
                    if len(targets) == 0:
                        globals.win = True
                    print 'Dropped off a box at the dropoff point.'
                    return

    def draw(self, canvas):
        g = globals.grid_size
        canvas.draw_circle([g*self.x, g*self.y], g/2, 1, 'black', 'blue')
        nose_line = {'right': ([g*self.x, g*self.y], [g*self.x+g, g*self.y]),
                'left': ([g*self.x, g*self.y], [g*self.x-g, g*self.y]),
                'up': ([g*self.x, g*self.y], [g*self.x, g*self.y-g]),
                'down': ([g*self.x, g*self.y], [g*self.x, g*self.y+g])}
        canvas.draw_line(nose_line[self.direction][0], nose_line[self.direction][1], 5, 'blue')


class dropoff_point():
    def __init__(self, x, y):
        self.x, self.y = x, y
        global blocked_coordinates
        globals.blocked_coordinates.add((x,y))
    
    def draw(self, canvas):
        g = globals.grid_size
        canvas.draw_polygon([(g*self.x - g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y - g/2),
                             (g*self.x + g/2, g*self.y + g/2),
                             (g*self.x - g/2, g*self.y + g/2)],
                          1, 'blue', 'yellow')

class target():
    def __init__(self, x, y, points):
        self.x, self.y = x, y
        self.points = points
        self.collected = False
        self.being_carried = False

    def draw(self, canvas):
        if not self.collected:
            g = globals.grid_size
            canvas.draw_polygon([(g*self.x - g/2, g*self.y - g/2),
                                 (g*self.x + g/2, g*self.y - g/2),
                                 (g*self.x + g/2, g*self.y + g/2),
                                 (g*self.x - g/2, g*self.y + g/2)],
                    1, 'blue', 'white')

            canvas.draw_text(str(self.points), [g*self.x - 5, g*self.y + 5], 8, 'blue')

class barrier():
    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_left, self.top_right, self.bottom_right, self.bottom_left = top_left, top_right, bottom_right, bottom_left

        #global blocked_coordinates
        for x in range(self.top_left[0], self.top_right[0]+1):
            for y in range(self.top_left[1], self.bottom_left[1]+1):
                globals.blocked_coordinates.add((x,y))

    def draw(self, canvas):
        g = globals.grid_size
        canvas.draw_polygon([tuple(g*coord for coord in self.top_left), tuple(g*coord for coord in self.top_right), \
            tuple(g*coord for coord in self.bottom_right), tuple(g*coord for coord in self.bottom_left)], 1, 'black', 'green')



