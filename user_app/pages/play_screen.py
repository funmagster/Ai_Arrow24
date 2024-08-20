import asyncio
import threading
import wave
import pygame
import pyaudio

from config import *
from registry import Registry
from pages.pages import Pages
from func.func_pages import (
    draw_text_box_in_play, resize_box,
    get_params_rect, base64_to_pygame_image,
    resize_icon
)
from func.music import play_next_track, recognize_speech


class PlayScreen(Pages):
    def __init__(self):
        super().__init__()
        self.screen = Registry.get('screen')
        self.font = Registry.get('settings_page_font')
        self.states = {
            'state': None,
            'is_loading': False,
            'finish_loading': False,
            'ok_loading': True,
            'response': None,
            'recording': False,
            'text': None,
            'is_ok_text': None,
        }
        self.count_room_complete = 0
        self.first_load = True
        self.response_ready = False
        self.p = pyaudio.PyAudio()
        self.microphone_icon = pygame.image.load(MICROPHONE_ICON)
        self.stream = None
        self.frames = []
        self.is_finish = False

        self.toggle_button = pygame.Rect(PLAY_RECT_VIS_TEXT)
        self.is_text_visible = True

        # Initialize UI components
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components and their positions."""
        width, height = self.screen.get_size()

        # Scale and position the microphone icon
        self.microphone_icon = pygame.transform.scale(
            self.microphone_icon, resize_icon(width, height, MICROPHONE_ICON_RECT)
        )
        self.icon_rect = self.microphone_icon.get_rect(
            right=width - MICROPHONE_ICON_RECT_indent[0],
            bottom=height - MICROPHONE_ICON_RECT_indent[1]
        )

        # Resize and position the input text box
        self.rect_input_text = pygame.Rect(
            *resize_box(width, height, (PLAY_Page_RECT_X, PLAY_Page_RECT_Y, PLAY_Page_RECT_W, PLAY_Page_RECT_H))
        )

    def draw(self):
        """Render the current screen state."""
        if not self.background:
            self.background = base64_to_pygame_image(Registry.get('img'))

        if self.first_load:
            characters = '\n\n'.join(Registry.get('characters')[0])
            self.text = f"Вот список персонажей\n\n{characters}\n\n{Registry.get('history')}\nВаши действия?"
            self.first_load = False
        elif self.states['is_loading']:
            # Text is updated during loading
            pass
        elif self.response_ready:
            self._update_history()
            if not self.is_finish:
                self.text = f"{Registry.get('answer')}\nВаши действия?"
            else:
                self.text = f"{Registry.get('answer')}\nИгра закончена!"

        self.set_background()
        if not self.is_finish:
            self._draw_ui_elements()
        if self.states['is_ok_text'] is False:
            self._draw_error_text()

        # Recalculate the text box size in case of screen size changes
        width, height = self.screen.get_size()
        self.rect_input_text = pygame.Rect(
            *resize_box(width, height, (PLAY_Page_RECT_X, PLAY_Page_RECT_Y, PLAY_Page_RECT_W, PLAY_Page_RECT_H))
        )

    def _update_history(self):
        """Append the latest answer to the history."""
        history = Registry.get('history')
        answer = Registry.get('answer')
        Registry.set('history', history + answer)

    def _draw_ui_elements(self):
        """Draw UI elements like the text box and microphone icon."""
        width, height = self.screen.get_size()

        # Update icon size and position
        self.microphone_icon = pygame.transform.scale(
            self.microphone_icon, resize_icon(width, height, MICROPHONE_ICON_RECT)
        )
        self.icon_rect = self.microphone_icon.get_rect(
            right=width - MICROPHONE_ICON_RECT_indent[0],
            bottom=height - MICROPHONE_ICON_RECT_indent[1]
        )

        # Draw text box and microphone icon only if text is visible
        if self.is_text_visible:
            draw_text_box_in_play(
                self.screen, self.text,
                get_params_rect(self.rect_input_text),
                font=self.font,
                color_rect=BLACK_OPACITY,
                color_font=WHITE,
                font_size=Play_font_size
            )

        # Draw the microphone icon
        self.screen.blit(self.microphone_icon, self.icon_rect)

        # Draw the toggle button
        pygame.draw.rect(self.screen, PLAY_Button_color, self.toggle_button)  # Button color
        button_font = pygame.font.Font(None, 24)
        button_text = button_font.render("Выключить/включить текст", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.toggle_button.center)
        self.screen.blit(button_text, button_text_rect)

    def _draw_error_text(self):
        """Display error messages when speech recognition fails."""
        if self.is_text_visible:
            font = pygame.font.Font(None, 20)
            error_texts = ["Я тебя не раслышал.", "Попробуй снова"]
            y_positions = [self.icon_rect.top - 20, self.icon_rect.top - 10]

            for text, y_pos in zip(error_texts, y_positions):
                self._draw_centered_text(font, text, (255, 0, 0), y_pos)

    def _draw_centered_text(self, font, text, color, y_pos):
        """Draw centered text at a specified vertical position."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.icon_rect.centerx, y_pos))
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle user events such as button clicks."""
        self.states['state'] = None

        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['play'], self.current_track)
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.is_finish:
            if self.icon_rect.collidepoint(event.pos):
                self.start_recording()
            elif self.toggle_button.collidepoint(event.pos):
                # Toggle text visibility
                self.is_text_visible = not self.is_text_visible
                # If voice text was recognized, ensure it is visible
                if self.states['is_ok_text']:
                    self.is_text_visible = True
        elif event.type == pygame.MOUSEBUTTONUP and not self.is_finish:
            if self.icon_rect.collidepoint(event.pos) and self.states['recording']:
                self.stop_recording()
                if self.states['is_ok_text']:
                    self._handle_valid_input()

        return self.states

    def _handle_valid_input(self):
        """Process valid input and request new data."""
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
        """Start recording audio from the microphone."""
        self.frames = []
        self.states['recording'] = True
        self.states['is_ok_text'] = None  # Reset text status before recording

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
        """Stop recording and process the recorded audio."""
        if self.stream:
            self.states['recording'] = False
            self.stream.stop_stream()
            self.stream.close()

            # Save recorded audio to a file
            with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(self.frames))

            # Recognize speech from the recorded audio
            self.states['is_ok_text'] = None
            self.states['text'], self.states['is_ok_text'] = recognize_speech()

            if self.states['is_ok_text']:
                self.is_text_visible = True
                self.text = f"{self.states['text']}\nЗагрузка..."
                self.states['is_loading'] = True

            self.p.terminate()
            self.p = pyaudio.PyAudio()
            self.stream = None

    async def finish_load_data(self):
        """Handle the completion of data loading and update the screen accordingly."""
        try:
            if self.states['response']['status_code'] == 200:
                self.first_load = False
                Registry.set('answer', self.states['response']['answer'])
                Registry.set('action', self.states['response']['action'])
                Registry.set('history', self.states['response']['history'])

                self.current_track = play_next_track(
                    LOADING_MUSIC_PLAYLIST['play'], self.states['response']['music']
                )

                if self.states['response']['action'] == 4:
                    self.is_finish = True

                if self.states['response']['img']:
                    self.background = None
                    Registry.set('img', self.states['response']['img'])

                self.response_ready = True
            else:
                self.states['state'] = 'error'
                print(f"Error: Received status code {self.states['response']['status_code']}")
        except Exception:
            self.states['state'] = 'error'

        self.states['is_loading'] = False
        self.states['finish_loading'] = False
        self.states['ok_loading'] = None
        return self.states
