import random

try: import simplegui
except:
    print 'Could not load simplegui. Loading simpleguitk instead'
    import sys
    if '/home/mch/Code/Python' not in sys.path: sys.path.append('/home/mch/Code/Python')
    import simpleguitk as simplegui

#configuration options
grid_size = 15
board_size = [40, 30]
keys = {38: 'up', 39: 'right', 40: 'down', 37: 'left'}
targets = set([])
dropoff_points = set([])
blocked_coordinates = set([])
barriers = set([])
win = False
has_moved = False

def draw_handler(canvas):
    p.draw(canvas)
    for target in targets:
        target.draw(canvas)
    for dropoff_point in dropoff_points:
        dropoff_point.draw(canvas)
    for barrier in barriers:
        barrier.draw(canvas)
    canvas.draw_text(str(p.score), [grid_size * (board_size[0]-3), grid_size * (board_size[1]-2)], 30, 'blue')

    if not has_moved:
        canvas.draw_text('Collect the boxes and carry them to the yellow dropoff points. Avoid the green barriers.', [20, 100], 16, 'blue')

    if win:
        canvas.draw_text('You win! Close the window and restart to play again', [20, 100], 18, 'blue')
    
def keydown_handler(keycode):
    global has_moved
    has_moved = True
    try:
        key = keys[keycode]
        if key == 'right': p.move_right()
        if key == 'down': p.move_down()
        if key == 'left': p.move_left()
        if key == 'up': p.move_up()
    except: print 'Invalid key press. Need to use arrow keys'
    

class player():
    def __init__(self):
        self.x, self.y = 0, 0
        self.direction = 'right'
        self.score = 0
        self.carrying_box = False

    def move_up(self):
        if (self.x, self.y - grid_size) not in blocked_coordinates: self.y -= grid_size
        self.direction = 'up'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x, self.y - grid_size

    def move_down(self):
        if (self.x, self.y + grid_size) not in blocked_coordinates: self.y += grid_size
        self.direction = 'down'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x, self.y + grid_size

    def move_right(self):
        if (self.x + grid_size, self.y) not in blocked_coordinates: self.x += grid_size
        self.direction = 'right'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x + grid_size, self.y

    def move_left(self):
        if (self.x - grid_size, self.y) not in blocked_coordinates: self.x -= grid_size
        self.direction = 'left'
        self.did_i_score()
        self.pick_up_box()
        if self.carrying_box: self.carrying_box.x, self.carrying_box.y = self.x - grid_size, self.y

    def pick_up_box(self):
        if not self.carrying_box:
            for box in targets:
                if box.x == self.x and box.y == self.y:
                    box.being_carried = True
                    self.carrying_box = box
                    print 'Player picked up a box'

    def did_i_score(self):
        if self.carrying_box:
            for dropoff_point in dropoff_points:
                if self.carrying_box.x == dropoff_point.x and self.carrying_box.y == dropoff_point.y:
                    self.score += self.carrying_box.points
                    self.carrying_box.collected = True
                    self.carrying_box.being_carried = False
                    global targets
                    targets.remove(self.carrying_box)
                    self.carrying_box = False
                    if len(targets) == 0:
                        global win
                        win = True
                    print 'Dropped off a box at the dropoff point.'
                    return

    def draw(self, canvas):
        canvas.draw_circle([self.x, self.y], grid_size/2, 1, 'black', 'blue')
        nose_line = {'right': ([self.x + grid_size/2, self.y], [self.x + grid_size, self.y]),
                'left': ([self.x - grid_size/2, self.y], [self.x - grid_size, self.y]),
                'up': ([self.x, self.y - grid_size/2], [self.x, self.y - grid_size]),
                'down': ([self.x, self.y + grid_size/2], [self.x, self.y + grid_size])}
        canvas.draw_line(nose_line[self.direction][0], nose_line[self.direction][1], 5, 'blue')


class dropoff_point():
    def __init__(self, x, y):
        self.x, self.y = x, y
        global blocked_coordinates
        blocked_coordinates.add((x,y))
    
    def draw(self, canvas):
        canvas.draw_polygon([(self.x - grid_size/2, self.y-grid_size/2),
                        (self.x + grid_size/2, self.y - grid_size/2),
                        (self.x + grid_size/2, self.y + grid_size/2),
                        (self.x - grid_size/2, self.y + grid_size/2)],
                    1, 'blue', 'yellow')

class target():
    def __init__(self, x, y, points):
        self.x, self.y = x, y
        self.points = points
        self.collected = False
        self.being_carried = False

    def draw(self, canvas):
        if not self.collected:
            canvas.draw_polygon([(self.x - grid_size/2, self.y-grid_size/2),
                        (self.x + grid_size/2, self.y - grid_size/2),
                        (self.x + grid_size/2, self.y + grid_size/2),
                        (self.x - grid_size/2, self.y + grid_size/2)],
                    1, 'blue', 'white')

            canvas.draw_text(str(self.points), [self.x - 5, self.y + 5], 8, 'blue')

class barrier():
    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_left, self.top_right, self.bottom_right, self.bottom_left = top_left, top_right, bottom_right, bottom_left
        global blocked_coordinates
        for x in range(self.top_left[0], self.top_right[0]+1, grid_size):
            for y in range(self.top_left[1], self.bottom_left[1]+1, grid_size):
                blocked_coordinates.add((x,y))

    def draw(self, canvas):
        canvas.draw_polygon([self.top_left, self.top_right, self.bottom_right, self.bottom_left], 1, 'black', 'green')


frame = simplegui.create_frame('Walking Player', grid_size * board_size[0], grid_size * board_size[1])
frame.set_canvas_background('white')
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(keydown_handler)

p = player()

for i in range(0,10):
    x = random.randrange(1, board_size[0])*grid_size
    y = random.randrange(1, board_size[1])*grid_size
    points = random.randint(1,5)*5
    targets.add(target(x, y, points))

for i in range(0,2):
    x = random.randrange(1, board_size[0])*grid_size
    y = random.randrange(1, board_size[1])*grid_size
    dropoff_points.add(dropoff_point(x,y))

barriers.add(barrier((15*grid_size, 10*grid_size), (17*grid_size, 10*grid_size), (17*grid_size, 15*grid_size), (15*grid_size, 15*grid_size)))

for target in targets:
    if (target.x, target.y) in blocked_coordinates: targets.remove(target)


frame.start()
