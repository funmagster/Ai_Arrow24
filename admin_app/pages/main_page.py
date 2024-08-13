from config import *
from registry import Registry, Pages
from func.func_pages import resize_box

class MainScreen(Pages):
    def __init__(self):
        self.background = Registry.get('main_screen_background')
        self.screen = Registry.get('screen')
        self.font = Registry.get('main_page_font')
        self.MAX_WIDTH = Registry.get('MAX_WIDTH')
        self.MAX_HEIGHT = Registry.get('MAX_HEIGHT')
        self.active_textbox = False

        widht, height = self.screen.get_size()
        self.textbox_rect = self.resize_textbox(widht, height)
        self.input_text = ''
        self.state = None
        self.fullscreen = False

    def draw(self):
        self.set_background()

        widht, height = self.screen.get_size()
        self.textbox_rect = self.resize_textbox(widht, height)

        pygame.draw.rect(self.screen, GRAY, self.textbox_rect, 2, 20)
        txt_surface = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(txt_surface,
                         (self.textbox_rect.x + self.textbox_rect.w // 2 - 52, self.textbox_rect.y + 8))

    def resize_textbox(self, new_width, new_height):
        self.fullscreen = False
        if new_width == self.MAX_WIDTH - 20 or new_height == self.MAX_HEIGHT - 60:
            new_width, new_height = self.MAX_WIDTH, self.MAX_HEIGHT
            self.fullscreen = True

        textbox_x, textbox_y, textbox_w, textbox_h = resize_box(
            new_width,
            new_height,
            (Main_Page_RECT_X, Main_Page_RECT_Y, Main_Page_RECT_W, Main_Page_RECT_H)
        )

        if self.fullscreen:
            return pygame.Rect(textbox_x - 30, textbox_y - 50, textbox_w - 30, textbox_h)
        return pygame.Rect(textbox_x, textbox_y, textbox_w, textbox_h)

    def handle_event(self, event):
        self.state = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            widht, height = self.screen.get_size()
            textbox_rect = self.resize_textbox(widht, height)
            if textbox_rect.collidepoint(event.pos):
                self.active_textbox = True
            else:
                self.active_textbox = False

        elif event.type == pygame.KEYDOWN and self.active_textbox:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active_textbox = False
                self.input_animation(end=True)

                if self.input_text == '12345':
                    self.state = 'settings'
                else:
                    txt_error = self.font.render("Ключ не подходит!", True, RED)
                    if self.fullscreen:
                        self.screen.blit(txt_error,
                                         (self.textbox_rect.x + 60, self.textbox_rect.y + 90))
                    else:
                        self.screen.blit(txt_error,
                                         (self.textbox_rect.x, self.textbox_rect.y + 60))
                    pygame.display.update()
                    pygame.time.delay(1000)

            elif len(self.input_text) <= 5 and event.unicode.isdigit():
                self.input_text += event.unicode
        self.input_animation(end=not self.active_textbox)
        return self.state
