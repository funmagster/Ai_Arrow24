from registry import Registry
from pages.pages import Pages
from func.music import play_next_track
from config import *


class ErrorScreen(Pages):
    def __init__(self):
        super().__init__()
        self.background = Registry.get('error_screen_background')
        self.screen = Registry.get('screen')
        self.MAX_WIDTH = Registry.get('MAX_WIDTH')
        self.MAX_HEIGHT = Registry.get('MAX_HEIGHT')
        self.current_track = 0

        self.states = {
            'state': None, 'is_loading': False,
            'finish_loading': False, 'ok_loading': True,
            'response': None
        }

    def draw(self):
        self.set_background()

    def handle_event(self, event):
        self.states['state'] = None

        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['error'], self.current_track)

        return self.states
