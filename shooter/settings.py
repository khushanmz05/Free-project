# Screen
WIDTH, HEIGHT = 900, 600
FPS = 60
TITLE = "AI Shooter"

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
PLAYER_SPEED      = 4
PLAYER_MAX_HP     = 100
PLAYER_SIZE       = 20
PLAYER_COLOR      = GREEN
BULLET_SPEED      = 10
BULLET_SIZE       = 5
BULLET_COLOR      = YELLOW
SHOOT_COOLDOWN    = 200   # ms

# Enemy
ENEMY_SPEED       = 1.8
ENEMY_SIZE        = 18
ENEMY_HP          = 30
ENEMY_COLOR       = RED
ENEMY_BULLET_SPEED = 6
ENEMY_SHOOT_RANGE  = 300  # px — only shoots if closer than this
ENEMY_SHOOT_CD     = 1500 # ms

# Walls
WALL_COLOR        = GREY
WALL_THICKNESS    = 20