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
timers = set([])

maximum_order = 10
orders_per_minute = 2

order_timeout = 25

max_tote_size = 5
totes_per_minute = 8
divert_odds = .5


game_over = False
has_moved = False
has_diverted = False

picker = None
packer = None

active_player = None
inactive_player = None

player_default_speed = 1.0/10
default_conveyor_speed = 1.0/30
divert_speed = 1.0/240

order = False

#odds are implied __/100
divert_y = 9
divert_x = 3
divert_end_x = 15

up = False
right = False
down = False
left = False


instructions = {'move': 'Use arrow keys to move the player.', 
            'divert': 'Most totes are heading to other zones of the warehouse.', 
            'pack': 'A tote has arrived in your zone! Take it to a blue empty bay.', 
            'order': 'The most popular items arrive with the most inventory',
            'change_player': 'An order! Use space bar to change control to the picker.',
            'pick': 'Collect the items from each orange bay.',
            'ship': 'Deliver order to the yellow ship station before time runs out.',
            'play_game': '',
            'gameover': 'Game Over'}

progress_steps = ['move', 'divert', 'pack', 'order', 'change_player', 'pick', 'ship', 'play_game', 'gameover']
progress_completed = {'move': False, 'divert': False, 'pack': False, 'order': False, 'change_player': False, 
                             'pick': False, 'ship': False, 'play_game': False, 'gameover': False}
