import pygame
from config import WAVE_OUTPUT_FILENAME
import speech_recognition as sr


def play_next_track(playlist, current_track):
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

    current_track = (current_track + 1) % len(playlist)
    return current_track


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='ru-RU'), True
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio", False
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e), False