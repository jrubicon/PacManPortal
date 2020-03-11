from pygame.math import Vector2 as vect

# Game Settings
HS_FILE = "highscore.txt"
# Screen Settings
WIDTH, HEIGHT = 610, 670
FPS = 60
PM_WIDTH, PM_HEIGHT = WIDTH - 50, HEIGHT - 50

INTRO_TEXT_SIZE = 30
LOGO = 60
LOGO_FONT = 'arial'
INTRO_FONT = 'arial'

ROWS = 30
COLS = 28

PLAYBUTTON = ((WIDTH//2-80), (HEIGHT//2+170))
HIGHSCORESBUTTON = ((WIDTH//2-88), (HEIGHT//2+220))

RESTARTBUTTON = ((WIDTH//2-88), (HEIGHT//2+10))
QUITBUTTON = ((WIDTH//2-88), (HEIGHT//2+70))

# Color Settings
BLACK = (0, 0, 0)
ORANGE = (250, 150, 19)
PURPLE = (142, 85, 255)
BLUE = (0, 0, 255)
RED = (250, 0, 0)
GRAY = (107, 107, 107)
WHITE = (255, 255, 255)
COIN = (255, 255, 0)
POWERUP = (255, 255, 255)

# Player Settings
#PLAYERSTARTPOS = vect(14,17)

PLAYERCOLOR = (255, 255, 0)
SPEED = 5
# Ghost Settings
