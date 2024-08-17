import pygame
from config import MIN_WIDTH, MIN_HEIGHT
import base64
import io
from PIL import Image


def wrap_text(text, font, max_width, color):
    """
        Разбивает текст на строки, чтобы каждая строка не превышала указанную ширину.

        :param text: Строка текста, который нужно перенести
        :param font: Объект шрифта Pygame для вычисления размера текста
        :param max_width: Максимальная ширина строки
        :return: Список строк, где каждая строка имеет ширину не больше max_width
    """
    words = text.split(' ')
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


def resize_icon(new_width, new_height, icon_size):
    w, h = icon_size

    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_w = w * scale_x
    new_h = h * scale_y
    return new_w, new_h


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


def base64_to_pygame_image(base64_string):
    """
    Преобразует строку base64 в объект Pygame Surface.

    :param base64_string: Строка base64, представляющая изображение.
    :return: Объект Pygame Surface.
    """
    # Декодирование строки base64 в бинарные данные
    image_data = base64.b64decode(base64_string)

    # Преобразование бинарных данных в изображение с помощью Pillow
    image = Image.open(io.BytesIO(image_data))

    # Преобразование изображения Pillow в формат, который понимает Pygame
    # Переопределяем формат в Pygame для корректного отображения
    if image.mode == 'RGBA':
        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, 'RGBA')
    elif image.mode == 'RGB':
        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, 'RGB')
    elif image.mode == 'L':
        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, 'L')
    else:
        raise ValueError(f"Unsupported image mode: {image.mode}")

    return pygame_image


def draw_text_box_in_play(surface, text, rect, font, color_rect, color_font, font_size, line_spacing=10):
    """
    Рисует текстовый блок с текстом, который автоматически переносится на следующую строку.
    :param surface: Поверхность, на которой рисуется текст
    :param text: Текст для отображения
    :param rect: Прямоугольник, определяющий место и размеры текстового блока (x, y, width, height)
    :param font: Объект шрифта Pygame для отрисовки текста
    :param color_rect: Цвет заполнения прямоугольника в формате RGBA (включая альфа-канал)
    :param color_font: Цвет шрифта
    :param font_size: Размер шрифта
    :param line_spacing: Расстояние между строками
    """
    x, y, width, height = rect

    # Создаем временную поверхность с альфа-каналом
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # Заливаем поверхность цветом с прозрачностью
    rect_surface.fill(color_rect)

    # Отображаем временную поверхность на основной поверхности
    surface.blit(rect_surface, (x, y))

    # Рисуем границу прямоугольника
    pygame.draw.rect(surface, (0, 0, 0), rect, 2)  # Граница черного цвета и толщиной 2

    # Переносим текст с учетом символов новой строки и расстояния между строками
    y_offset = 10
    for line in text.split('\n'):
        wrapped_lines = wrap_text_2(line, font, width - 20)
        for wrapped_line in wrapped_lines:
            text_surface = font.render(wrapped_line, True, color_font)
            surface.blit(text_surface, (x + 10, y + y_offset))
            y_offset += font_size + line_spacing
        y_offset += line_spacing  # Добавляем немного дополнительного отступа между абзацами


def wrap_text_2(text, font, max_width):
    """
    Переносит текст по строкам, чтобы они не выходили за заданную ширину.
    :param text: Исходный текст
    :param font: Объект шрифта Pygame
    :param max_width: Максимальная ширина строки
    :return: Список строк, которые не превышают max_width
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Пробуем добавить слово в текущую строку
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines