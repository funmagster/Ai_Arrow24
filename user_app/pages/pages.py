import pygame
from func.func_pages import background_resize
from func.rooms_api import fetch_data


class Pages:
    def __init__(self):
        # Initialize common attributes
        self.background = None
        self.screen = None
        self.font = None
        self.input_text = ''
        self.states = {
            'state': None,
            'is_loading': False,
            'finish_loading': False,
            'ok_loading': True,
            'response': None
        }
        self.active_textbox = False
        self.current_track = 0

    def reset_states(self):
        """Reset the states to their initial values."""
        self.input_text = ''
        self.states = {
            'state': None,
            'is_loading': False,
            'finish_loading': False,
            'ok_loading': True,
            'response': None
        }
        self.active_textbox = False
        self.current_track = 0

    def set_background(self):
        screen_width, screen_height = self.screen.get_size()
        bg_width, bg_height = self.background.get_size()
        new_width, new_height, x, y = background_resize(
            screen_width, screen_height, bg_width, bg_height
        )

        resized_background = pygame.transform.scale(self.background,
                                                    (int(new_width),
                                                     int(new_height)))
        self.screen.blit(resized_background, (x, y))

    def input_animation(self, end):
        if len(self.input_text) and self.input_text[-1] == '|':
            self.input_text = self.input_text[:-1].replace("|", '')
        elif end:
            self.input_text = self.input_text.replace("|", '')
        else:
            self.input_text += '|'

    async def load_data(self, data, path):
        try:
            self.states['response'] = await fetch_data(data, path)
        except Exception as e:
            self.states['state'] = 'error'

        self.states['is_loading'] = False
        self.states['finish_loading'] = True

    def draw(self):
        ...

    def handle_event(self, event):
        ...

