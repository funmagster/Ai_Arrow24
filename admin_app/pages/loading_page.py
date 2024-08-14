import asyncio
import cv2
import numpy as np
from registry import Registry, Pages
from func.music import play_next_track
import concurrent.futures
from config import *


class LoadingScreen(Pages):
    def __init__(self):
        self.screen = Registry.get('screen')
        self.current_frame = 0
        self.cap = cv2.VideoCapture(LOADING_VIDEO_PATH)
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.loop = asyncio.get_event_loop()
        self.resize_video()
        self.future = None
        self.current_track = 0
        self.states = {
            'state': None, 'is_loading': True,
            'finish_loading': False, 'ok_loading': True,
            'response': None
        }

    def resize_video(self):
        # Получаем размеры видео
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def draw(self):
        # Получаем размеры экрана
        screen_width, screen_height = self.screen.get_size()
        # Вычисляем размеры видео с учетом соотношения сторон
        video_width = screen_width
        video_height = int(video_width / ASPECT_RATIO)
        if video_height > screen_height:
            video_height = screen_height
            video_width = int(video_height * ASPECT_RATIO)
        x_offset = (screen_width - video_width) // 2
        y_offset = (screen_height - video_height) // 2

        # Захват и отображение кадра
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (video_width, video_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
            self.screen.blit(frame_surface, (x_offset, y_offset))
        else:
            # Видео закончено
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['loading'], self.current_track)
        return self.states

    def __del__(self):
        # Освобождение ресурсов
        self.cap.release()

    async def finish_load_data(self):
        if self.states['response']['status_code'] == 200:
            self.states['state'] = 'main'
            self.states['ok_loading'] = True
        else:
            self.states['ok_loading'] = False
        self.states['finish_loading'] = False
        return self.states