# global variables
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'impact'
TITLE = "Boingo"
HS_FILE = 'highscore.txt'

# player properties
PLAYER_ACC = .5
PLAYER_FRICTION = -.1
PLAYER_GRAVITY = .5
PLAYER_JUMP = 15

# starting platforms
PLATFORM_LIST = [(0, HEIGHT - 20, 100, 20),
                 (200, HEIGHT - 100, 200, 20),
                 (100, HEIGHT - 250, 200, 20),
                 (0, HEIGHT - 400, 200, 20),
                 (150, HEIGHT - 550, 100, 20),
                 (50, HEIGHT - 700, 200, 20),
                 (400, HEIGHT - 850, 100, 20),
                 (300, HEIGHT - 1000, 100, 20),
                 (0, HEIGHT - 1150, 200, 20),
                 (50, HEIGHT - 1300, 100, 20),
                 (200, HEIGHT - 1450, 100, 20)]

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 200, 0)