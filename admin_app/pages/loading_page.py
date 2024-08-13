import asyncio
import cv2
import numpy as np
from registry import Registry, Pages
from func.rooms_api import fetch_data
from func.music import play_next_track
import concurrent.futures
from config import *


class LoadingScreen(Pages):
    def __init__(self):
        self.screen = Registry.get('screen')
        self.is_loading = True
        self.current_frame = 0
        self.cap = cv2.VideoCapture(LOADING_VIDEO_PATH)
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.loop = asyncio.get_event_loop()
        self.resize_video()
        self.future = None
        self.current_track = 0

    def resize_video(self):
        # Получаем размеры видео
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def draw(self):
        if self.is_loading:
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
        else:
            self.screen.fill((0, 0, 0))

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST, self.current_track)

    async def load_data(self):
        data = {'name': '12346'}
        data = await fetch_data(data, '/rooms/join_room')
        self.is_loading = False
        return data

    def check_loading_complete(self):
        if self.future and self.future.done():
            try:
                data = self.future.result()
                self.is_loading = False
                # Обработайте данные, если необходимо
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self.is_loading = False

    def __del__(self):
        # Освобождение ресурсов
        self.cap.release()
