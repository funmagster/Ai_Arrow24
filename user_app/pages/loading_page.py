import asyncio
import cv2
import numpy as np
import pygame
import concurrent.futures
from registry import Registry
from pages.pages import Pages
from func.music import play_next_track
from config import *


class LoadingScreen(Pages):
    def __init__(self):
        super().__init__()
        self.video_height = None
        self.video_width = None
        self.screen = Registry.get('screen')
        self.current_frame = 0
        self.cap = cv2.VideoCapture(LOADING_VIDEO_PATH)
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.loop = asyncio.get_event_loop()
        self.resize_video()
        self.future = None
        self.current_track = 0
        self.states = {
            'state': None,
            'is_loading': True,
            'finish_loading': False,
            'ok_loading': True,
            'response': None,
            'first': True
        }

    def resize_video(self):
        # Retrieve video dimensions
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def draw(self):
        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()
        # Compute video dimensions maintaining aspect ratio
        video_width = screen_width
        video_height = int(video_width / ASPECT_RATIO)
        if video_height > screen_height:
            video_height = screen_height
            video_width = int(video_height * ASPECT_RATIO)
        x_offset = (screen_width - video_width) // 2
        y_offset = (screen_height - video_height) // 2

        # Capture and display frame
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (video_width, video_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
            self.screen.blit(frame_surface, (x_offset, y_offset))
        else:
            # Reset video if it ends
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def handle_event(self, event):
        # Handle user event and update track
        self.states['state'] = None
        if event.type == pygame.USEREVENT + 1:
            self.current_track = play_next_track(LOADING_MUSIC_PLAYLIST['loading'], self.current_track)
        return self.states

    def __del__(self):
        # Release video capture resource
        self.cap.release()

    async def finish_load_data(self):
        try:
            if self.states['response']['status_code'] == 200:
                if self.states['first']:
                    # Store initial response data in the registry
                    Registry.set('story', self.states['response']['story'])
                    Registry.set('history', self.states['response']['history'])
                    Registry.set('characters', self.states['response']['characters'])
                    Registry.set('img', self.states['response']['img'])
                    self.states['first'] = False
                else:
                    # Update registry with new response data
                    Registry.set('answer', self.states['response']['answer'])
                    Registry.set('action', self.states['response']['action'])
                    Registry.set('img', self.states['response']['img'])
                self.states['state'] = 'play'
                self.states['ok_loading'] = True
            else:
                self.states['ok_loading'] = False
        except Exception:
            self.states['state'] = 'error'
        self.states['finish_loading'] = False
        return self.states
