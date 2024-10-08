import pygame
from dotenv import load_dotenv
import os

pygame.init()
load_dotenv()


# Project settings
Title = "DnD organizer"
url_backend = os.getenv('server_url')
MIN_WIDTH, MIN_HEIGHT = 960, 540
FPS = 30
ASPECT_RATIO = MIN_WIDTH / MIN_HEIGHT

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
COLOR_BUTTON = (187, 131, 199)
COLOR_TEXT_RECT = (255, 117, 207)
RED = (250, 10, 10)

# Font
FONT_SIZE = 60
font = pygame.font.Font(None, FONT_SIZE)

# Size
RECT_BUTTON = (250, 300, 500, 70)
RECT_Q = (300, 100, 400, 70)
RECT_PASSWORD = (400, 200, 200, 70)
PDF_BUTTON_REC = (250, 430, 500, 70)

# Coords
X_ROOM = 500
Y_ROOM = 400

# Content path
BACKGROUND = 'content/admin-background.png'
ICON = 'content/icon_admin.png'
