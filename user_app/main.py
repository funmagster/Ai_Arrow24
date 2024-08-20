import random

import aiohttp
import pygame
import asyncio
import sys
from config import *
from registry import Registry
from pages.main_page import MainScreen
from pages.settings_screen import SettingsScreen
from pages.loading_page import LoadingScreen
from pages.play_screen import PlayScreen
from pages.error_page import ErrorScreen
from func.music import play_next_track


def init_app():
    """
    Initialize the application settings
    """
    screen_info = pygame.display.Info()
    max_width, max_height = screen_info.current_w, screen_info.current_h

    # Store maximum screen dimensions in the Registry
    Registry.set('MAX_WIDTH', max_width)
    Registry.set('MAX_HEIGHT', max_height)

    # Set up the application icon
    icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(icon)

    # Initialize the screen in a resizable mode
    screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), pygame.RESIZABLE)
    Registry.set('screen', screen)
    pygame.display.set_caption("Dungeons and Dragons")
    Registry.set('FULLSCREEN', False)

    # Load and set all backgrounds and fonts into the Registry
    Registry.set_all(backgrounds, pygame.image.load)
    Registry.set_all(fonts)

    # Initialize the mixer and play background music
    pygame.mixer.init()
    pygame.mixer.music.load(START_MUSIC_PATH)
    pygame.mixer.music.set_volume(set_volume_start)
    pygame.mixer.music.play(-1)

    return max_width, max_height


class Main:
    """
    Main class to handle game logic and screen management
    """
    def __init__(self, max_width, max_height):
        pygame.init()
        self.screens = {
            'main': MainScreen(),
            'settings': SettingsScreen(),
            'loading': LoadingScreen(),
            'play': PlayScreen(),
            'error': ErrorScreen()
        }
        self.current_screen = 'main'
        self.screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        # Store max dimensions and initial states
        self.max_width = max_width
        self.max_height = max_height
        self.run_game = False
        self.loading = True

    def resize_screen(self, new_width, new_height):
        """
        Resize screen with constraints and aspect ratio handling
        """
        screen_mode = pygame.RESIZABLE
        if new_width >= self.max_width or new_height >= self.max_height:
            self.width = self.max_width - 20
            self.height = self.max_height - 60
        elif new_width < MIN_WIDTH or new_height < MIN_HEIGHT:
            self.width = MIN_WIDTH
            self.height = MIN_HEIGHT
        else:
            self.width = min(new_width, ASPECT_RATIO * new_height)
            self.height = min(new_height, new_width / ASPECT_RATIO)

        return self.width, self.height, screen_mode

    async def run(self):
        """
        Main loop to run the game asynchronously
        """
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
                    self.switch_screen(states['state'])

                    if self.current_screen == 'loading':
                        await self.handle_loading_screen()

            if self.current_screen != 'loading':
                self.screen.fill(BLACK)

            # Draw the current screen and update display
            self.screens[self.current_screen].draw()
            pygame.display.update()
            await asyncio.sleep(1 / FPS)

    def switch_screen(self, new_screen):
        """
        Switch to a new screen and handle music transition
        """
        self.current_screen = new_screen
        pygame.mixer.music.stop()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        track = random.randint(0, len(LOADING_MUSIC_PLAYLIST[self.current_screen]) - 1)
        play_next_track(LOADING_MUSIC_PLAYLIST[self.current_screen], track)
        self.screens[self.current_screen].current_track = track

    async def handle_loading_screen(self):
        """
        Handle actions specific to the loading screen
        """
        if not self.run_game:
            self.run_game = True
            room = Registry.get('room')
            prompt = Registry.get('prompt')
            try:
                asyncio.create_task(self.screens['loading'].load_data(
                    data={"prompt": prompt, 'room': room},
                    path='/game/start_game'
                ))
            except Exception:
                self.current_screen = 'error'
            self.loading = False
        elif self.loading:
            self.loading = False
            self.screens[self.current_screen].reset_states()


if __name__ == "__main__":
    pygame.init()
    max_width, max_height = init_app()
    app = Main(max_width, max_height)
    asyncio.run(app.run())
