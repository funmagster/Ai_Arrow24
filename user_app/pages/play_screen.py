import asyncio

from config import *
from registry import Registry, Pages
from func.func_pages import (
    draw_text_box_in_play, resize_box,
    get_params_rect, base64_to_pygame_image,
    resize_icon
)
from func.music import play_next_track, recognize_speech
import threading
import pyaudio
import wave


class PlayScreen(Pages):
    def __init__(self):
        super().__init__()
        self.screen = Registry.get('screen')
        self.background = None
        self.font = Registry.get('settings_page_font')
        self.states = {
            'state': None, 'is_loading': False,
            'finish_loading': False, 'ok_loading': True,
            'response': None, 'recording': False,
            'text': None, 'is_ok_text': None,
        }
        self.count_room_complete = 0
        self.first_load = True
        self.response_ready = False
        self.p = pyaudio.PyAudio()
        self.microphone_icon = pygame.image.load(MICROPHONE_ICON)
        self.stream = None
        self.frames = []
        self._init_ui()
        self.is_finish = False

    def _init_ui(self):
        widht, height = self.screen.get_size()
        self.microphone_icon = pygame.transform.scale(
            self.microphone_icon, resize_icon(widht, height, MICROPHONE_ICON_RECT)
        )
        self.icon_rect = self.microphone_icon.get_rect(
            right=widht - MICROPHONE_ICON_RECT_indent[0],
            bottom=height - MICROPHONE_ICON_RECT_indent[1]
        )
        self.rect_input_text = pygame.Rect(
            *resize_box(
                widht, height,
                (PLAY_Page_RECT_X, PLAY_Page_RECT_Y, PLAY_Page_RECT_W, PLAY_Page_RECT_H)
            )
        )

    def draw(self):
        if self.background is None:
            self.background = base64_to_pygame_image(Registry.get('img'))

        if self.first_load:
            characters = '\n\n'.join(Registry.get('characters')[0])
            self.text = f"Вот список персонажей\n\n{characters}\n\n{Registry.get('history')}\nВаши действия?"
            self.first_load = False
        elif self.states['is_loading']:
            # Если идет загрузка, текст уже был обновлен на "Идет загрузка..." в stop_recording
            pass
        elif self.response_ready:  # Обновление текста только после получения ответа
            self._update_history()
            self.text = f"{Registry.get('answer')}\nВаши действия?"

        self.set_background()
        if not self.is_finish:
            self._draw_ui_elements()

        if self.states['is_ok_text'] is False:
            self._draw_error_text()

        widht, height = self.screen.get_size()
        self.rect_input_text = pygame.Rect(
            *resize_box(
                widht, height,
                (PLAY_Page_RECT_X, PLAY_Page_RECT_Y, PLAY_Page_RECT_W, PLAY_Page_RECT_H)
            )
        )

    def _update_history(self):
        history = Registry.get('history')
        answer = Registry.get('answer')
        Registry.set('history', history + answer)

    def _draw_ui_elements(self):
        widht, height = self.screen.get_size()
        self.microphone_icon = pygame.transform.scale(
            self.microphone_icon, resize_icon(
                widht, height, MICROPHONE_ICON_RECT
            )
        )
        self.icon_rect = self.microphone_icon.get_rect(
            right=widht - MICROPHONE_ICON_RECT_indent[0],
            bottom=height - MICROPHONE_ICON_RECT_indent[1]
        )
        draw_text_box_in_play(
            self.screen, self.text,
            get_params_rect(self.rect_input_text),
            font=self.font,
            color_rect=BLACK_OPACITY,
            color_font=WHITE,
            font_size=Play_font_size
        )
        self.screen.blit(self.microphone_icon, self.icon_rect)

    def _draw_error_text(self):
        font = pygame.font.Font(None, 20)
        error_text_1 = "Я тебя не раслышал."
        error_text_2 = "Попробуй еще раз"
        self._draw_centered_text(font, error_text_1, (255, 0, 0), self.icon_rect.top - 20)
        self._draw_centered_text(font, error_text_2, (255, 0, 0), self.icon_rect.top - 10)

    def _draw_centered_text(self, font, text, color, y_pos):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.icon_rect.centerx, y_pos))
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        self.states['state'] = None
        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['play'], self.current_track)
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.is_finish:
            if self.icon_rect.collidepoint(event.pos):
                self.start_recording()
        elif event.type == pygame.MOUSEBUTTONUP and not self.is_finish:
            if self.icon_rect.collidepoint(event.pos) and self.states['recording']:
                self.stop_recording()
                if self.states['is_ok_text']:
                    self._handle_valid_input()

        return self.states

    def _handle_valid_input(self):
        self.count_room_complete += 1
        characters = '\n\n'.join(Registry.get('characters')[0])
        Registry.set('history', Registry.get('history') + self.states['text'])
        data = {
            'room': Registry.get('room'),
            'prompt': self.states['text'],
            'character': characters,
            'count_room_complete': self.count_room_complete,
            'history': Registry.get('history'),
            'story': Registry.get('story')
        }
        asyncio.create_task(self.load_data(data=data, path='/game/play'))
        self.states['is_loading'] = True
        self.states['is_ok_text'] = None
        self.states['text'] = None

    def start_recording(self):
        self.frames = []
        self.states['recording'] = True
        self.states['is_ok_text'] = None  # Сбрасываем перед началом записи

        self.stream = self.p.open(
            format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            frames_per_buffer=CHUNK
        )
        print("Recording started...")

        def record():
            while self.states['recording']:
                data = self.stream.read(CHUNK)
                self.frames.append(data)

        threading.Thread(target=record).start()

    def stop_recording(self):
        if self.stream:
            self.states['recording'] = False
            self.stream.stop_stream()
            self.stream.close()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            self.states['is_ok_text'] = None  # Сбрасываем перед распознаванием
            self.states['text'], self.states['is_ok_text'] = recognize_speech()

            if self.states['is_ok_text']:
                # Отображаем текст, который сказал пользователь, и сообщение о загрузке
                self.text = f"{self.states['text']}\nИдет загрузка..."
                self.states['is_loading'] = True

            self.p.terminate()
            self.p = pyaudio.PyAudio()
            self.stream = None

    async def finish_load_data(self):
        if self.states['response']['status_code'] == 200:
            self.first_load = False
            Registry.set('answer', self.states['response']['answer'])
            Registry.set('action', self.states['response']['action'])
            Registry.set('history', self.states['response']['history'])

            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['play'], self.states['response']['music'])

            if self.states['response']['action'] == 4:
                self.is_finish = True
            if not self.states['response']['img'] is None:
                self.background = None
                Registry.set('img', self.states['response']['img'])
            self.response_ready = True  # Устанавливаем флаг после получения ответа
        else:
            print(f"Error: Received status code {self.states['response']['status_code']}")

        self.states['is_loading'] = False
        self.states['finish_loading'] = False
        self.states['ok_loading'] = None
        return self.states

