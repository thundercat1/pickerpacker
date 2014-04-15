
#configuration options
grid_size = 20 
g = grid_size
board_size = [30, 25]
keys = {38: 'up', 39: 'right', 40: 'down', 37: 'left', 32: 'space'}
totes = set([])
dropoff_points = set([])
blocked_coordinates = set([])
barriers = set([])

bays = set([])

win = False
has_moved = False

picker = None
packer = None

active_player = None
inactive_player = None

player_default_speed = 1.0/15
up = False
right = False
down = False
left = False
