from config import *
from registry import Registry, Pages
from func.func_pages import draw_text_box, resize_box, get_params_rect


class SettingsScreen(Pages):
    def __init__(self):
        self.background = Registry.get('settings_screen_background')
        self.screen = Registry.get('screen')
        self.font = Registry.get('settings_page_font')
        self.input_text = ''
        self.state = None
        self.active_textbox = False

        widht, height = self.screen.get_size()
        self.rect_input_text = pygame.Rect(
            *resize_box(
                widht, height,
                (Settings_Page_RECT_X, Settings_Page_RECT_Y, Settings_Page_RECT_W, Settings_Page_RECT_H)
            )
        )

    def draw(self):
        self.set_background()

        widht, height = self.screen.get_size()
        self.rect_input_text = pygame.Rect(
            *resize_box(
                widht, height,
                (Settings_Page_RECT_X, Settings_Page_RECT_Y, Settings_Page_RECT_W, Settings_Page_RECT_H)
            )
        )

        draw_text_box(
            self.screen, self.input_text,
            get_params_rect(self.rect_input_text),
            font=self.font,
            color_rect=WHITE,
            color_font=WHITE,
            font_size=Settings_font_size
        )

    def handle_event(self, event):
        self.state = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_input_text.collidepoint(event.pos):
                self.active_textbox = True
            else:
                self.active_textbox = False

        elif event.type == pygame.KEYDOWN and self.active_textbox:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]

            elif event.key == pygame.K_RETURN:
                self.active_textbox = False
                self.input_animation(end=True)

                if len(self.input_text.split()) >= 5:
                    self.state = 'loading'
                else:
                    txt_error = self.font.render("Введите больше 5 слов!", True, RED)
                    self.screen.blit(
                        txt_error,
                        (self.rect_input_text.x + self.rect_input_text.w // 2 - 150,
                         self.rect_input_text.y + self.rect_input_text.h + 20)
                    )
                    pygame.display.update()
                    pygame.time.delay(1000)

            elif len(self.input_text) <= 200:
                if event.key == pygame.K_SPACE:
                    self.input_text += ' '
                elif event.unicode:
                    self.input_text += event.unicode

        self.input_animation(end=not self.active_textbox)
        return self.state
