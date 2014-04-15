
#configuration options
grid_size = 15
g = grid_size
board_size = [40, 30]
keys = {38: 'up', 39: 'right', 40: 'down', 37: 'left'}
targets = set([])
dropoff_points = set([])
blocked_coordinates = set([])
barriers = set([])
win = False
has_moved = False

p = None
player_default_speed = 1.0/15
up = False
right = False
down = False
left = False
