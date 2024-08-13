import pygame
from config import MIN_WIDTH, MIN_HEIGHT


def wrap_text(text, font, max_width, color):
    """
        Разбивает текст на строки, чтобы каждая строка не превышала указанную ширину.

        :param text: Строка текста, который нужно перенести
        :param font: Объект шрифта Pygame для вычисления размера текста
        :param max_width: Максимальная ширина строки
        :return: Список строк, где каждая строка имеет ширину не больше max_width
    """
    words = text.split()
    lines = []
    current_line = ''

    for word in words:
        test_line = f'{current_line} {word}'.strip()
        test_surface = font.render(test_line, True, color)
        test_width, _ = test_surface.get_size()
        if test_width > max_width:
            if current_line:
                lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    return lines


def draw_text_box(surface, text,
                  rect, font, color_rect,
                  color_font, font_size):
    """
        Рисует текстовый блок с текстом, который автоматически переносится на следующую строку.

        :param surface: Поверхность, на которой рисуется текст
        :param text: Текст для отображения
        :param rect: Прямоугольник, определяющий место и размеры текстового блока (x, y, width, height)
        :param font: Объект шрифта Pygame для отрисовки текста
    """
    x, y, width, height = rect
    pygame.draw.rect(surface, color_rect, rect, 2, 30)  # Рисуем границу прямоугольника

    lines = wrap_text(text, font, width - 20, color=color_font)  # Учитываем отступы
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color_font)
        surface.blit(text_surface, (x + 10, y + 10 + i * font_size))


def resize_box(new_width, new_height, rect):
    rect_x, rect_y, rect_w, rect_h = rect

    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_x = rect_x * scale_x
    new_y = rect_y * scale_y
    new_w = rect_w * scale_x
    new_h = rect_h * scale_y
    return new_x, new_y, new_w, new_h


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


def get_params_rect(rect: pygame.Rect):
    return rect.x, rect.y, rect.w, rect.h
