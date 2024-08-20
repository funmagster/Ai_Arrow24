import pygame
from config import *


def draw_text(
        text: str, font: pygame.font.Font,
        color: tuple, surface: pygame.Surface,
        x: int, y: int
):
    """
    Renders and draws text on a surface at the specified position.

    Args:
        text (str): The text to render.
        font (pygame.font.Font): The font object to render the text.
        color (tuple): Color of the text (R, G, B).
        surface (pygame.Surface): The surface to draw the text on.
        x (int): X-coordinate for text placement.
        y (int): Y-coordinate for text placement.
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def background_resize(
        screen_width: int, screen_height: int,
        bg_width: int, bg_height: int
) -> tuple:
    """
    Resizes the background to fit within the screen dimensions while maintaining aspect ratio.

    Args:
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        bg_width (int): The width of the background image.
        bg_height (int): The height of the background image.

    Returns:
        tuple: New dimensions and position (new_width, new_height, x, y) for the background.
    """
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


def resize_box(new_width: int, new_height: int, rect: tuple) -> tuple:
    """
    Resizes a rectangle proportionally based on new dimensions.

    Args:
        new_width (int): The new width after resizing.
        new_height (int): The new height after resizing.
        rect (tuple): The original rectangle (x, y, width, height).

    Returns:
        tuple: The resized rectangle (new_x, new_y, new_width, new_height).
    """
    rect_x, rect_y, rect_w, rect_h = rect

    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_x = rect_x * scale_x
    new_y = rect_y * scale_y
    new_w = rect_w * scale_x
    new_h = rect_h * scale_y
    return new_x, new_y, new_w, new_h


def adapt_font_size(screen_width: int) -> int:
    """
    Adjusts font size proportionally to the screen width.

    Args:
        screen_width (int): The width of the screen.

    Returns:
        int: The adapted font size.
    """
    return int(FONT_SIZE * (screen_width / MIN_WIDTH))


def draw_rect_with_alpha(
        screen: pygame.Surface, color: tuple,
        rect: pygame.Rect, alpha: int, border_radius: int
):
    """
    Draws a rectangle with transparency (alpha) on the screen.

    Args:
        screen (pygame.Surface): The surface to draw the rectangle on.
        color (tuple): The color of the rectangle (R, G, B).
        rect (pygame.Rect): The rectangle's dimensions and position.
        alpha (int): The transparency level (0-255).
        border_radius (int): The radius of the rectangle's corners.
    """
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(temp_surface, (*color, alpha), temp_surface.get_rect(), border_radius=border_radius)
    screen.blit(temp_surface, rect.topleft)


def resize_text_pos(new_width: int, new_height: int, x: int, y: int) -> tuple:
    """
    Resizes text position proportionally based on new dimensions.

    Args:
        new_width (int): The new width after resizing.
        new_height (int): The new height after resizing.
        x (int): The original x-coordinate of the text.
        y (int): The original y-coordinate of the text.

    Returns:
        tuple: The new coordinates (new_x, new_y) for the text.
    """
    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_x = x * scale_x
    new_y = y * scale_y
    return new_x, new_y
