import asyncio
import pygame
from config import *
from registry import Registry
from pages.pages import Pages
from func.func_pages import resize_box
from func.music import play_next_track


class MainScreen(Pages):
    def __init__(self):
        super().__init__()
        self.background = Registry.get('main_screen_background')
        self.screen = Registry.get('screen')
        self.font = Registry.get('main_page_font')
        self.MAX_WIDTH = Registry.get('MAX_WIDTH')
        self.MAX_HEIGHT = Registry.get('MAX_HEIGHT')
        self.active_textbox = False
        self.current_track = 0

        width, height = self.screen.get_size()
        self.textbox_rect = self.resize_textbox(width, height)
        self.input_text = ''
        self.fullscreen = False

        # Initialize state tracking for screen and loading status
        self.states = {
            'state': None,
            'is_loading': False,
            'finish_loading': False,
            'ok_loading': True,
            'response': None
        }

    def draw_message_text(self, txt_error):
        """
        Method to draw an error message on the screen
        """
        x_offset = 60 if self.fullscreen else 0
        y_offset = 90 if self.fullscreen else 60
        self.screen.blit(txt_error, (self.textbox_rect.x + x_offset, self.textbox_rect.y + y_offset))

    def draw(self):
        """
        Main drawing function for the screen
        """
        self.set_background()
        width, height = self.screen.get_size()
        self.textbox_rect = self.resize_textbox(width, height)
        pygame.draw.rect(self.screen, GRAY, self.textbox_rect, 2, 20)

        txt_surface = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(txt_surface, (self.textbox_rect.x + self.textbox_rect.w // 2 - 52, self.textbox_rect.y + 8))

        if self.states['is_loading']:
            self.draw_message_text(self.font.render("Идет загрузка...", True, RED))
        elif not self.states['ok_loading']:
            self.draw_message_text(self.font.render("Ключ не подходит", True, RED))

    def resize_textbox(self, new_width, new_height):
        """
        Resizes the textbox based on screen size, maintaining aspect ratio
        """
        self.fullscreen = new_width == self.MAX_WIDTH - 20 or new_height == self.MAX_HEIGHT - 60

        textbox_x, textbox_y, textbox_w, textbox_h = resize_box(
            new_width,
            new_height,
            (Main_Page_RECT_X, Main_Page_RECT_Y, Main_Page_RECT_W, Main_Page_RECT_H)
        )

        if self.fullscreen:
            return pygame.Rect(textbox_x - 30, textbox_y - 50, textbox_w - 30, textbox_h)
        return pygame.Rect(textbox_x, textbox_y, textbox_w, textbox_h)

    def handle_event(self, event):
        """
        Event handler for user interactions on the main screen
        """
        self.states['state'] = None

        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['main'], self.current_track)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            width, height = self.screen.get_size()
            textbox_rect = self.resize_textbox(width, height)
            self.active_textbox = textbox_rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active_textbox and not self.states['is_loading']:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active_textbox = False
                self.states['is_loading'] = True
                asyncio.create_task(self.load_data(
                    data={'name': self.input_text.replace('|', '')},
                    path='/rooms/join_room'
                ))
            elif len(self.input_text) <= 5 and event.unicode.isdigit():
                self.input_text += event.unicode

        self.input_animation(end=not self.active_textbox)
        return self.states

    async def finish_load_data(self):
        """
        Handles the completion of data loading and transitions to the appropriate screen"""
        try:
            response = self.states['response']
            if response['status_code'] == 200:
                self.states['state'] = 'settings'
                room_name = self.input_text.replace('|', '')
                Registry.set('room', room_name)
                self.states['ok_loading'] = True
            else:
                self.states['ok_loading'] = False

        except Exception:
            self.states['ok_loading'] = False
            self.states['state'] = 'error'  # Switch to the error screen on server error

        finally:
            self.states['finish_loading'] = False

        return self.states
