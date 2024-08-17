import random

import pygame
import asyncio
import sys
from config import *
from registry import Registry
import pages
from func.music import play_next_track


def init_app():
    screen_info = pygame.display.Info()
    MAX_WIDTH, MAX_HEIGHT = screen_info.current_w, screen_info.current_h
    Registry.set('MAX_WIDTH', MAX_WIDTH)
    Registry.set('MAX_HEIGHT', MAX_HEIGHT)
    icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), pygame.RESIZABLE)
    Registry.set('screen', screen)
    pygame.display.set_caption("Dungeons and dragons")

    Registry.set('FULLSCREEN', False)

    # Set backgrounds
    for name_background, path_to_background in backgrounds.items():
        Registry.set(name_background, pygame.image.load(path_to_background))

    # Set fonts
    for name_font, font in fonts.items():
        Registry.set(name_font, font)

    pygame.mixer.init()
    pygame.mixer.music.load(START_MUSIC_PATH)
    pygame.mixer.music.set_volume(set_volume_start)
    pygame.mixer.music.play(-1)

    return MAX_WIDTH, MAX_HEIGHT


class Main:
    def __init__(self, MAX_WIDTH, MAX_HEIGHT):
        pygame.init()
        self.screens = {
            'main': pages.MainScreen(),
            'settings': pages.SettingsScreen(),
            'loading': pages.LoadingScreen(),
            'play': pages.PlayScreen()
        }
        self.current_screen = 'main'
        self.width = MIN_WIDTH
        self.height = MIN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.MAX_WIDTH = MAX_WIDTH
        self.MAX_HEIGHT = MAX_HEIGHT

        self.run_game = False
        self.loading = True
        self.history = []

    def resize_screen(self, new_width, new_height):
        screen_mode = pygame.RESIZABLE
        if new_width == self.MAX_WIDTH or new_height == self.MAX_HEIGHT:
            self.width = self.MAX_WIDTH - 20
            self.height = self.MAX_HEIGHT - 60
        elif new_width < MIN_WIDTH or new_height < MIN_HEIGHT:
            self.width = MIN_WIDTH
            self.height = MIN_HEIGHT
        elif new_width != self.width:
            self.width = new_width
            self.height = new_width / ASPECT_RATIO
        else:
            self.width = ASPECT_RATIO * new_height
            self.height = new_height
        return self.width, self.height, screen_mode

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    new_width, new_height = event.size
                    set_width, set_height, mode_screen = self.resize_screen(new_width, new_height)
                    self.screen = pygame.display.set_mode((set_width, set_height), mode_screen)

                states = self.screens[self.current_screen].handle_event(event)

                if states['finish_loading']:
                    states = await self.screens[self.current_screen].finish_load_data()

                if states['state']:
                    self.current_screen = states['state']
                    pygame.mixer.music.stop()
                    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
                    track = random.randint(0, len(LOADING_MUSIC_PLAYLIST[self.current_screen]) - 1)
                    play_next_track(LOADING_MUSIC_PLAYLIST[self.current_screen], track)
                    self.screens[self.current_screen].current_track = track
                    if self.current_screen == 'loading' and not self.run_game:
                        self.run_game = True
                        room = Registry.get('room')
                        prompt = Registry.get('prompt')
                        asyncio.create_task(self.screens['loading'].load_data(
                            data={"prompt": prompt,
                                  'room': room},
                            path='/game/start_game'
                        ))
                        self.loading = False
                    elif self.current_screen == 'loading' and self.loading:
                        self.loading = False
                        self.screens[self.current_screen].states['state'] = None
                        self.screens[self.current_screen].states['response'] = None

            if self.current_screen != 'loading':
                self.screen.fill(BLACK)
            self.screens[self.current_screen].draw()
            pygame.display.update()
            await asyncio.sleep(1 / FPS)


if __name__ == "__main__":
    pygame.init()
    MAX_WIDTH, MAX_HEIGHT = init_app()
    app = Main(MAX_WIDTH, MAX_HEIGHT)

    # Run the main loop in an asynchronous event loop
    asyncio.run(app.run())
