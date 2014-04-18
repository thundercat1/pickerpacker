#configuration options
grid_size = 30 
tote_font_size = 14

frame = None

board_size = [None, None]
keys = {38: 'up', 39: 'right', 40: 'down', 37: 'left', 32: 'space'}
totes = []
dropoff_points = set([])
blocked_coordinates = set([])
barriers = set([])
score = 0
bays = set([])
pickable_inventory = []
maximum_order = 10
max_tote_size = 1

win = False
has_moved = False

picker = None
packer = None

active_player = None
inactive_player = None

player_default_speed = 1.0/15
default_conveyor_speed = 1.0/30
divert_speed = 1.0/240
tote_spawn_delay = 4000
order_spawn_delay = 15000
order = False

#odds are implied __/100
divert_odds = 50
divert_y = 9
divert_x = 3
divert_end_x = 15

up = False
right = False
down = False
left = False
