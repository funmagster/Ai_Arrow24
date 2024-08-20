import pygame
from config import MIN_WIDTH, MIN_HEIGHT
import base64
import io
from PIL import Image


def wrap_text(text, font, max_width, color):
    """
    Wraps the text into lines that do not exceed the specified width.

    :param text: The text string to be wrapped
    :param font: Pygame font object for measuring text size
    :param max_width: Maximum width of a line
    :param color: Color of the text (not used in this function but could be for rendering)
    :return: List of lines where each line does not exceed max_width
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


def draw_text_box(surface, text, rect, font, color_rect, color_font, font_size):
    """
    Draws a text box with text that wraps to the next line automatically.

    :param surface: The surface to draw the text on
    :param text: The text to display
    :param rect: Rectangle defining the position and size of the text box (x, y, width, height)
    :param font: Pygame font object for rendering text
    :param color_rect: Color of the rectangle border
    :param color_font: Color of the text
    :param font_size: Size of the font
    """
    x, y, width, height = rect
    pygame.draw.rect(surface, color_rect, rect, 2, 30)  # Draw rectangle border

    lines = wrap_text(text, font, width - 20, color=color_font)  # Consider padding
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color_font)
        surface.blit(text_surface, (x + 10, y + 10 + i * font_size))


def resize_box(new_width, new_height, rect):
    """
    Resizes a rectangle based on the new width and height.

    :param new_width: New width of the canvas
    :param new_height: New height of the canvas
    :param rect: Original rectangle (x, y, width, height)
    :return: New rectangle with scaled dimensions
    """
    rect_x, rect_y, rect_w, rect_h = rect

    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_x = rect_x * scale_x
    new_y = rect_y * scale_y
    new_w = rect_w * scale_x
    new_h = rect_h * scale_y
    return new_x, new_y, new_w, new_h


def resize_icon(new_width, new_height, icon_size):
    """
    Resizes an icon based on the new width and height.

    :param new_width: New width of the canvas
    :param new_height: New height of the canvas
    :param icon_size: Original icon size (width, height)
    :return: New icon size with scaled dimensions
    """
    w, h = icon_size

    scale_x = new_width / MIN_WIDTH
    scale_y = new_height / MIN_HEIGHT

    new_w = w * scale_x
    new_h = h * scale_y
    return new_w, new_h


def background_resize(screen_width, screen_height, bg_width, bg_height):
    """
    Resizes the background to fit the screen while maintaining the aspect ratio.

    :param screen_width: Width of the screen
    :param screen_height: Height of the screen
    :param bg_width: Width of the background image
    :param bg_height: Height of the background image
    :return: New width, new height, and position (x, y) to center the background
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


def get_params_rect(rect: pygame.Rect):
    """
    Extracts parameters from a Pygame Rect object.

    :param rect: Pygame Rect object
    :return: Tuple of (x, y, width, height)
    """
    return rect.x, rect.y, rect.w, rect.h


def base64_to_pygame_image(base64_string):
    """
    Converts a base64 string to a Pygame Surface object.

    :param base64_string: Base64 string representing an image
    :return: Pygame Surface object
    """
    # Decode base64 string to binary data
    image_data = base64.b64decode(base64_string)

    # Convert binary data to an image using Pillow
    image = Image.open(io.BytesIO(image_data))

    # Convert Pillow image to a Pygame-compatible format
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
    Draws a text box with wrapped text that considers line spacing and new lines.

    :param surface: The surface to draw the text on
    :param text: The text to display
    :param rect: Rectangle defining the position and size of the text box (x, y, width, height)
    :param font: Pygame font object for rendering text
    :param color_rect: Fill color of the rectangle in RGBA format (including alpha channel)
    :param color_font: Color of the text
    :param font_size: Size of the font
    :param line_spacing: Spacing between lines
    """
    x, y, width, height = rect

    # Create a temporary surface with alpha channel
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # Fill surface with the background color with transparency
    rect_surface.fill(color_rect)

    # Blit the temporary surface onto the main surface
    surface.blit(rect_surface, (x, y))

    # Draw the border of the rectangle
    pygame.draw.rect(surface, (0, 0, 0), rect, 2)  # Black border with thickness 2

    # Render text with consideration for new lines and line spacing
    y_offset = 10
    for line in text.split('\n'):
        wrapped_lines = wrap_text_2(line, font, width - 20)
        for wrapped_line in wrapped_lines:
            text_surface = font.render(wrapped_line, True, color_font)
            surface.blit(text_surface, (x + 10, y + y_offset))
            y_offset += font_size + line_spacing
        y_offset += line_spacing  # Add extra spacing between paragraphs


def wrap_text_2(text, font, max_width):
    """
    Wraps text into lines that do not exceed the specified width.

    :param text: The text to be wrapped
    :param font: Pygame font object for measuring text size
    :param max_width: Maximum width of a line
    :return: List of lines where each line does not exceed max_width
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Attempt to add the word to the current line
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
