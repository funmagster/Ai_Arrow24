import pygame
from func.func_pages import background_resize
from func.rooms_api import fetch_data


class Registry:
    _shared_state = {}

    @classmethod
    def set(cls, key, value):
        cls._shared_state[key] = value

    @classmethod
    def get(cls, key):
        return cls._shared_state.get(key)


class Pages:
    def __init__(self):
        self.states = {
            'state': None, 'is_loading': False,
            'finish_loading': False, 'ok_loading': True,
            'response': None
        }
    def draw(self):
        ...

    def handle_event(self, event):
        ...

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
        self.states['response'] = await fetch_data(data, path)
        self.states['is_loading'] = False
        self.states['finish_loading'] = True