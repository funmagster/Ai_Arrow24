import pygame


def play_next_track(playlist, current_track):
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

    current_track = (current_track + 1) % len(playlist)
    return current_track
