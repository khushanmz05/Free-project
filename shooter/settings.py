# Screen
WIDTH, HEIGHT = 900, 600
FPS = 60
TITLE = "Run & Gun"

# Colors
BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
DARK_GREY  = (30, 30, 30)
GREY       = (80, 80, 80)
RED        = (220, 50, 50)
GREEN      = (50, 220, 100)
BLUE       = (50, 150, 220)
YELLOW     = (240, 200, 50)
ORANGE     = (240, 120, 30)

# Player
PLAYER_SPEED = 4
PLAYER_MAX_HP = 100
PLAYER_SIZE = 20
PLAYER_COLOR = GREEN
BULLET_SPEED = 10
BULLET_SIZE = 8
BULLET_COLOR = YELLOW
SHOOT_COOLDOWN = 200 # ms

# Enemy
ENEMY_SPEED = 1.8
ENEMY_SIZE = 18
ENEMY_HP = 30
ENEMY_COLOR = RED
ENEMY_BULLET_SPEED = 6
ENEMY_SHOOT_RANGE = 300
ENEMY_SHOOT_CD = 1500 # ms

# Walls
WALL_COLOR = GREY
WALL_THICKNESS = 20

# Wave progression — 6 waves with increasing point thresholds
WAVE_THRESHOLDS = [60, 120, 200, 300, 420, 0]

def wave_target(wave):
    """Points needed to complete a given wave index."""
    if wave >= len(WAVE_THRESHOLDS):
        return 500
    return WAVE_THRESHOLDS[wave]

def is_boss_wave(wave):
    return wave == 5

TOTAL_WAVES = 6