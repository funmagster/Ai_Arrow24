import pygame
from config import *


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)


def background_resize(screen_width, screen_height, bg_width, bg_height):
    screen_ratio = screen_width / screen_height
    bg_ratio = bg_width / bg_height

    if screen_ratio > bg_ratio:
        new_width = screen_height * bg_ratio
        new_height = screen_height
    else:
        new_width = screen_width
        new_height = screen_width / bg_ratio

    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2

    return new_width, new_height, x, y


def resize_box(new_width, new_height, rect):
    rect_x, rect_y, rect_w, rect_h = rect

    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_x = rect_x * scale_x
    new_y = rect_y * scale_y
    new_w = rect_w * scale_x
    new_h = rect_h * scale_y
    return new_x, new_y, new_w, new_h


def adapt_font_size(screen_width):
    return int(FONT_SIZE * (screen_width / MIN_WIDTH))


def draw_rect_with_alpha(screen, color, rect, alpha, border_radius):
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(temp_surface, (*color, alpha), temp_surface.get_rect(), border_radius=border_radius)

    screen.blit(temp_surface, rect.topleft)


def resize_text_pos(new_width, new_height, x, y):

    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_x = x * scale_x
    new_y = y * scale_y
    return new_x, new_y