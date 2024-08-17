from config import *
from registry import Registry, Pages
from func.func_pages import draw_text_box, resize_box, get_params_rect
from func.music import play_next_track


class SettingsScreen(Pages):
    def __init__(self):
        super().__init__()
        self.background = Registry.get('settings_screen_background')
        self.screen = Registry.get('screen')
        self.font = Registry.get('settings_page_font')
        self.input_text = ''
        self.states = {
            'state': None, 'is_loading': False,
            'finish_loading': False, 'ok_loading': True,
            'response': None
        }
        self.active_textbox = False
        self.current_track = 0

        widht, height = self.screen.get_size()
        self.rect_input_text = pygame.Rect(
            *resize_box(
                widht, height,
                (Settings_Page_RECT_X, Settings_Page_RECT_Y, Settings_Page_RECT_W, Settings_Page_RECT_H)
            )
        )

    def draw_message_text(self, txt_error):
        self.screen.blit(
            txt_error,
            (self.rect_input_text.x + self.rect_input_text.w // 2 - 150,
             self.rect_input_text.y + self.rect_input_text.h + 20)
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
        if not self.states['ok_loading']:
            txt_error = self.font.render("Введите больше 5 слов!", True, RED)
            self.draw_message_text(txt_error)

    def handle_event(self, event):
        self.states['state'] = None
        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['settings'], self.current_track)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_input_text.collidepoint(event.pos):
                self.active_textbox = True
            else:
                self.active_textbox = False

        elif event.type == pygame.KEYDOWN and self.active_textbox:
            if event.type == pygame.USEREVENT + 1:
                self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['settings'], self.current_track)

            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]

            elif event.key == pygame.K_RETURN:
                self.active_textbox = False
                self.input_animation(end=True)

                if len(self.input_text.split()) >= 5:
                    Registry.set('prompt', self.input_text.replace('|', ''))
                    self.states['state'] = 'loading'
                else:
                    self.states['ok_loading'] = False

            elif len(self.input_text) <= 200:
                if event.key == pygame.K_SPACE:
                    self.input_text += ' '
                elif event.unicode:
                    self.input_text += event.unicode

        self.input_animation(end=not self.active_textbox)
        return self.states
