BLOCK_HEALTH = {
    "wood": 100,
    "ice": 100,
    "stone": 100
}

BIRD_DAMAGE = {
    "red": {"wood": 60, "ice": 60, "stone": 60},
    "chuck": {"wood": 65, "ice": 60, "stone": 60},
    "blues": {"wood": 60, "ice": 66, "stone": 60},
    "bomb": {"wood": 60, "ice": 60, "stone": 65}
}  # To be tuned before submitting


BIRD_OPTIONS = ["red", "chuck", "blues", "bomb"]
BLOCK_OPTIONS = ["wood", "ice", "stone"]
WIDTH, HEIGHT = 1600, 900
GRAVITY = 1000
FPS = 120
CATAPULT_SIZE = (50 * (WIDTH/1400),100 * (WIDTH/1400))
MAX_RADIUS = 125
e=0.3
MAX_COLLISIONS = 5
fortress_width, fortress_height = 7,7  # To be tuned before submitting
BIRD_SIZE = round(35 * (WIDTH/1400))
BLOCK_SIZE = round(30 * (WIDTH/1400))
WINNER_TEXT_FONT = round(40 * (WIDTH/1400))
WHO_START_FONT = round(30 * (WIDTH/1400))
PLAYER_NAME_FONT = round(30 * (WIDTH/1400))
MAIN_FONT = round(50 * (WIDTH/1400))
BALL_SIZE = 17 * (WIDTH/1600)
FACTOR_RED = 1.01 # Rate at which red bird grows
FACTOR_CHUCK = 1.5 # Factor at which speed of chuck increases
GROUND = HEIGHT/7
NUM_FRAMES = 14