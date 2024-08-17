import sys
import pygame
import requests
from config import *
from pygame import font as pygame_font
from registry import Registry
from func import *

import os


def init_app():
    screen_info = pygame.display.Info()
    MAX_WIDTH, MAX_HEIGHT = screen_info.current_w, screen_info.current_h
    Registry.set("MAX_WIDTH", MAX_WIDTH)
    Registry.set("MAX_HEIGHT", MAX_HEIGHT)

    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(Title)

    return MAX_WIDTH, MAX_HEIGHT, screen

class Main:
    def __init__(self, MAX_WIDTH, MAX_HEIGHT, screen):
        self.MAX_WIDTH = MAX_WIDTH
        self.MAX_HEIGHT = MAX_HEIGHT
        self.screen = screen
        self.input_text = ''
        self.room_number = ''
        self.password_text = ''
        self.room = None
        self.background = pygame.image.load(BACKGROUND)
        self.loading = False

        self.active_input = None
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.button_rect = pygame.Rect(RECT_BUTTON)
        self.input_rect = pygame.Rect(RECT_Q)
        self.password_rect = pygame.Rect(RECT_PASSWORD)
        self.font = pygame.font.Font(None, adapt_font_size(self.width))

        self.placeholder_color = (200, 200, 200, 180)  # RGB + Alpha

        # Кнопка для выгрузки в PDF
        self.pdf_button_rect = pygame.Rect(PDF_BUTTON_REC)
        self.pdf_button_visible = False

        self.x_room, self.y_room = X_ROOM, Y_ROOM
        self.clock = pygame.time.Clock()

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

    def resize_screen(self, new_width, new_height):
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

        # Адаптация размеров и позиции кнопки
        new_button_rect = resize_box(self.width, self.height, RECT_BUTTON)
        self.button_rect = pygame.Rect(new_button_rect)

        # Адаптация размеров и позиции полей ввода
        new_input_rect = resize_box(self.width, self.height, RECT_Q)
        self.input_rect = pygame.Rect(new_input_rect)

        new_password_rect = resize_box(self.width, self.height, RECT_PASSWORD)
        self.password_rect = pygame.Rect(new_password_rect)

        # Адаптация шрифта
        self.font = pygame.font.Font(None, adapt_font_size(self.width))

        # Установка позиции и размера кнопки "Выгрузить в PDF"
        new_pdf_button_rect = resize_box(self.width, self.height, PDF_BUTTON_REC)
        self.pdf_button_rect = pygame.Rect(
            new_pdf_button_rect
        )

        # Установка позиции для текста номера комнаты
        self.x_room, self.y_room = resize_text_pos(self.width, self.height, X_ROOM, Y_ROOM)
        return self.width, self.height

    def draw(self):
        self.set_background()

        draw_rect_with_alpha(self.screen, COLOR_TEXT_RECT, self.input_rect, 200, 10)
        if self.input_text:
            draw_text(self.input_text, self.font, BLACK, self.screen, self.input_rect.centerx, self.input_rect.centery)
        else:
            draw_text("Секретный ключ", self.font, self.placeholder_color, self.screen, self.input_rect.centerx,
                      self.input_rect.centery)

        draw_rect_with_alpha(self.screen, COLOR_TEXT_RECT, self.password_rect, 180, 10)
        if self.password_text:
            draw_text(self.password_text, self.font, BLACK, self.screen, self.password_rect.centerx,
                      self.password_rect.centery)
        else:
            draw_text("Пароль", self.font, self.placeholder_color, self.screen, self.password_rect.centerx,
                      self.password_rect.centery)

        if self.loading:
            draw_text("Loading...", self.font, BLACK, self.screen, self.button_rect.centerx, self.button_rect.centery)
        else:
            draw_rect_with_alpha(self.screen, COLOR_BUTTON, self.button_rect, 200, 10)
            draw_text("Сгенерировать комнату", self.font, BLACK, self.screen, self.button_rect.centerx,
                      self.button_rect.centery)

        if self.room_number:
            draw_text(self.room_number, self.font, RED, self.screen, self.x_room, self.y_room)

        if self.pdf_button_visible:
            draw_rect_with_alpha(self.screen, COLOR_BUTTON, self.pdf_button_rect, 200, 10)
            draw_text("Выгрузить в PDF", self.font, BLACK, self.screen, self.pdf_button_rect.centerx,
                      self.pdf_button_rect.centery)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    new_width, new_height = event.size
                    set_width, set_height = self.resize_screen(new_width, new_height)
                    self.screen = pygame.display.set_mode((set_width, set_height), pygame.RESIZABLE)

                if event.type == pygame.KEYDOWN:
                    if self.active_input == 'input':
                        if event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        elif len(self.input_text) <= 5:
                            self.input_text += event.unicode
                    elif self.active_input == 'password':
                        if event.key == pygame.K_BACKSPACE:
                            self.password_text = self.password_text[:-1]
                        elif len(self.password_text) <= 5:
                            self.password_text += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_rect.collidepoint(event.pos):
                        self.active_input = 'input'
                    elif self.password_rect.collidepoint(event.pos):
                        self.active_input = 'password'
                    elif self.button_rect.collidepoint(event.pos) and self.input_text != ''\
                            and not self.loading and not self.pdf_button_visible:
                        self.loading = True
                        self.room_number = 'Loading...'
                        try:
                            param = {
                                'secret':  self.input_text,
                                'password': self.password_text,
                            }
                            response = requests.post(url_backend + '/rooms/create_room', json=param).json()
                            if response['status_code'] == 200:
                                self.room_number = f"Ваша комната: {response['room']}"
                                self.room = response['room']
                                self.pdf_button_visible = True
                            else:
                                self.room_number = f'Ключ неправильный!'
                        except Exception as e:
                            self.room_number = f'Error: {str(e)}'
                        self.loading = False

                    elif self.pdf_button_visible and self.pdf_button_rect.collidepoint(event.pos):
                        param = {
                            'name': self.room,
                            'password': self.password_text,
                        }
                        response = requests.post(url_backend + '/rooms/download_pdf', json=param)
                        if response.status_code == 200:
                            current_directory = os.getcwd()
                            with open(f"{current_directory}/downloaded_file.pdf", "wb") as f:
                                f.write(response.content)
                        else:
                            print(f"Failed to download file. Status code: {response.status_code}")

            self.screen.fill(BLACK)
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    MAX_WIDTH, MAX_HEIGHT, screen = init_app()
    app = Main(MAX_WIDTH, MAX_HEIGHT, screen)
    app.run()
