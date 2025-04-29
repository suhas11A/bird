import pygame # type: ignore

BLOCK_HEALTH = {
    "wood": 100,
    "ice": 100,
    "stone": 100,
    "iron" : 100
}

BIRD_DAMAGE = {
    "red": {"wood": 45, "ice": 45, "stone": 45, "iron": 0},
    "chuck": {"wood": 65, "ice": 40, "stone": 40, "iron": 0},
    "blues": {"wood": 40, "ice": 65, "stone": 40, "iron": 0},
    "bomb": {"wood": 40, "ice": 40, "stone": 65, "iron": 0}
}

DIFFICULTY_SETTINGS = {
    1: {"width": 2,  "height": 5,  "wind_max":  0},
    2: {"width": 3,  "height": 6,  "wind_max":  3},
    3: {"width": 4,  "height": 7,  "wind_max":  6},
    4: {"width": 4,  "height": 8,  "wind_max":  9},
}

BIRD_OPTIONS = ["red", "chuck", "blues", "bomb"]
BLOCK_OPTIONS = ["wood", "ice", "stone", "iron"]
WIDTH, HEIGHT = 1600, 900
GRAVITY = 1000
FPS = 120
CATAPULT_SIZE = (50 * (WIDTH/1400),100 * (WIDTH/1400))
DIFF_SIZE = (WIDTH/20, WIDTH/20)
PAUSE_SIZE = (WIDTH/25, WIDTH/25)
SOUND_SIZE = (WIDTH/32, WIDTH/32)
MAX_RADIUS = 125
e=0.3
MAX_COLLISIONS = 5
fortress_width, fortress_height = 7,7
BIRD_SIZE = round(35 * (WIDTH/1400))
BLOCK_SIZE = round(40 * (WIDTH/1400))
EXTRA_SMALL_FONT = round(25 * (WIDTH/1400))
SMALL_FONT = round(30 * (WIDTH/1400))
MED_FONT = round(40 * (WIDTH/1400))
BIG_FONT = round(50 * (WIDTH/1400))
BALL_SIZE = 17 * (WIDTH/1600)
FACTOR_RED = 1.01 # Rate at which red bird grows
FACTOR_CHUCK = 1.9 # Factor at which speed of chuck increases
THEMES = ["default", "space", "lava", "desert", "castle", "farm"]
GROUND_LEVEL = {
    "default" : (HEIGHT/7),
    "space" : -(HEIGHT),
    "desert" : (HEIGHT/13),
    "farm" : (HEIGHT/9),
    "castle" : (HEIGHT/8.6),
    "lava" : (HEIGHT/8)
}
TEXT_COLOR = {
    "default" : (0,0,0),
    "space" : (255,255,255),
    "desert" : (0,0,0),
    "farm" : (0,0,0),
    "castle" : (0,0,0),
    "lava" : (255,225,105)
}
THEME_BACKGROUNDS_PATH = {
    "default": "./media/images/backgrounds/default.png",
    "space": "./media/images/backgrounds/space.png",
    "desert": "./media/images/backgrounds/desert.png",
    "farm": "./media/images/backgrounds/farm.png",
    "castle": "./media/images/backgrounds/castle.png",
    "lava": "./media/images/backgrounds/lava.png"
}
NUM_FRAMES = 15
wind_period = 30
WIND_MUL = 60
TIME_LIMIT = 20
NOISE_SEED = 1234
BUTTON_W = round(216 * (WIDTH/1600))
BUTTON_H = round(70 * (WIDTH/1600))
IRON_COUNT = 2