import pygame
from config import WAVE_OUTPUT_FILENAME
import speech_recognition as sr


def play_next_track(playlist, current_track):
    """
    Loads and plays the next track in the playlist.

    :param playlist: List of file paths for the playlist
    :param current_track: Index of the currently playing track
    :return: Updated index of the current track
    """
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

    # Update to the next track in the playlist, wrap around if at the end
    current_track = (current_track + 1) % len(playlist)
    return current_track


def recognize_speech():
    """
    Recognizes speech from an audio file using Google's speech recognition.

    :return: Tuple containing the recognized text and a boolean indicating success
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = recognizer.record(source)
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio, language='ru-RU')
            return text, True
        except sr.UnknownValueError:
            # Handle case where speech is unintelligible
            return "Google Speech Recognition could not understand audio", False
        except sr.RequestError as e:
            # Handle case where the request to the recognition service fails
            return f"Could not request results from Google Speech Recognition service; {e}", False
