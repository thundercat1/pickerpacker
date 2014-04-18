import random
try:
    import simplegui
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

def draw_handler(canvas):
    p.draw(canvas)
    for target in targets:
        target.draw(canvas)
    canvas.draw_text(str(p.score), [grid_size * (board_size[0]-3), grid_size * (board_size[1]-2)], 30, 'blue')
    
def keydown_handler(keycode):
    key = keys[keycode]
    if key == 'right': p.move_right()
    if key == 'down': p.move_down()
    if key == 'left': p.move_left()
    if key == 'up': p.move_up()
    
def keyup_handler(keycode):
    key = keys[keycode]

class player():
    def __init__(self):
        self.x, self.y = 0, 0
        self.direction = 'right'
        self.score = 0
        self.carrying_box = False

    def move_up(self):
        self.y -= grid_size
        self.direction = 'up'
        self.did_i_score()

    def move_down(self):
        self.y += grid_size
        self.direction = 'down'
        self.did_i_score()

    def move_right(self):
        self.x += grid_size
        self.direction = 'right'
        self.did_i_score()

    def move_left(self):
        self.x -= grid_size
        self.direction = 'left'
        self.did_i_score()

    def did_i_score(self):
        for target in targets:
            if target.x == self.x and target.y == self.y:
                target.collected = 'True'
                self.score += target.points
                print 'Collected target for', target.points, 'points.'
                print 'Player score', self.score

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
    
    def draw(self):
        pass
        

class target():
    def __init__(self, x, y, points):
        self.x, self.y = x, y
        self.points = points
        self.collected = False

    def draw(self, canvas):
        if not self.collected:
            canvas.draw_polygon([(self.x - grid_size/2, self.y-grid_size/2),
                    (self.x + grid_size/2, self.y - grid_size/2),
                    (self.x + grid_size/2, self.y + grid_size/2),
                    (self.x - grid_size/2, self.y + grid_size/2)],
                    1, 'blue', 'white')

            canvas.draw_text(str(self.points), [self.x - 5, self.y + 5], 8, 'blue')

frame = simplegui.create_frame('Walking Player', grid_size * board_size[0], grid_size * board_size[1])
frame.set_canvas_background('white')
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

p = player()

for i in range(0,6):
    x = random.randrange(1, board_size[0])*grid_size
    y = random.randrange(1, board_size[1])*grid_size
    points = random.randint(1,5)*5
    targets.add(target(x, y, points))

frame.start()
