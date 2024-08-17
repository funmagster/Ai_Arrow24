import pygame
import pyaudio

pygame.init()


# API
url_backend = 'http://194.87.232.123:8000' #'http://127.0.0.1:8000'

# Project settings
prefix = ''
ICON_PATH = prefix + 'img/icon.png'

LOADING_VIDEO_PATH = prefix + 'video/Loading.mp4'
START_MUSIC_PATH = prefix +'aduio/start_screens/Start_screens.mp3'
LOADING_MUSIC_PLAYLIST = {
    'loading': [
        prefix + 'aduio/loading/Loading-1.mp3',
        prefix + 'aduio/loading/Loading-2.mp3',
        prefix + 'aduio/loading/Loading-3.mp3'
    ],
    'main': [
        prefix + 'aduio/start_screens/Start_screens.mp3'
    ],
    'settings': [
        prefix + 'aduio/start_screens/Start_screens.mp3'
    ],
    'play': [
        prefix + 'aduio/play/play-1.mp3',
        prefix + 'aduio/play/play-2.mp3',
        prefix + 'aduio/play/play-3.mp3',
        prefix + 'aduio/play/play-4.mp3',
        prefix + 'aduio/play/play-5.mp3',
        prefix + 'aduio/play/play-6.mp3',
        prefix + 'aduio/play/play-7.mp3',
    ]
}
MIN_WIDTH, MIN_HEIGHT = 960, 540
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (220, 20, 60)
set_volume_start = 0.5
FPS = 30

# Main Page
Main_Page_RECT_X, Main_Page_RECT_Y = 650, 413
Main_Page_RECT_W, Main_Page_RECT_H = 268, 45
Main_font_size = 40

# Settings Page
Settings_Page_RECT_X, Settings_Page_RECT_Y = 200, 200
Settings_Page_RECT_W, Settings_Page_RECT_H = 570, 240
Settings_font_size = 40

# Play Page
Play_font_size = 20
PLAY_Page_RECT_X, PLAY_Page_RECT_Y = 50, 50
PLAY_Page_RECT_W, PLAY_Page_RECT_H = 850, 450
BLACK_OPACITY = (0, 0, 0, 56)

MICROPHONE_ICON = prefix + 'img/microphone.png'
MICROPHONE_ICON_RECT = (70, 70)
MICROPHONE_ICON_RECT_indent = (50, 50)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# ASPECT_RATIO
ASPECT_RATIO = MIN_WIDTH / MIN_HEIGHT

backgrounds = {
    'main_screen_background': prefix + 'img/pages/Main_page_img.png',
    'settings_screen_background': prefix + 'img/pages/Settings_page_img.png'
}

fonts = {
    'default_font': pygame.font.SysFont(None, 55),
    'main_page_font': pygame.font.SysFont(None, Main_font_size),
    'settings_page_font': pygame.font.SysFont(None, Settings_font_size),
    'play_page_font': pygame.font.SysFont(None, Play_font_size)
}