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

BIRD_DAMAGE_POWER = {
    "red": {"wood": 40, "ice": 40, "stone": 40},
    "chuck": {"wood": 40, "ice": 10, "stone": 10},
    "blues": {"wood": 10, "ice": 40, "stone": 10},
    "bomb": {"wood": 10, "ice": 10, "stone": 40}
}  # To be tuned before submitting


BIRD_OPTIONS = ["red", "chuck", "blues", "bomb"]
BLOCK_OPTIONS = ["wood", "ice", "stone"]
WIDTH, HEIGHT = 1600, 900
GRAVITY = 1000
FPS = 120
CATAPULT_SIZE = (50 * (WIDTH/1400),100 * (WIDTH/1400))
MAX_RADIUS = 100
e=0.3
MAX_COLLISIONS = 5
fortress_width, fortress_height = 1,1  # To be tuned before submitting
BIRD_SIZE = round(35 * (WIDTH/1400))
BLOCK_SIZE = round(30 * (WIDTH/1400))
WINNER_TEXT_FONT = round(40 * (WIDTH/1400))
WHO_START_FONT = round(30 * (WIDTH/1400))
PLAYER_NAME_FONT = round(30 * (WIDTH/1400))
MAIN_FONT = round(50 * (WIDTH/1400))
BALL_SIZE = 17 * (WIDTH/1600)