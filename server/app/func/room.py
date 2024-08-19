from app.db.db import get_history
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import textwrap
import os


def string_to_pdf(text, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Регистрация шрифта, поддерживающего кириллицу
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    text_object = c.beginText(40, height - 40)
    text_object.setFont("DejaVuSans", 12)

    # Устанавливаем максимальную ширину текста
    max_width = width - 80  # Оставляем отступы по краям

    # Высота строки в пикселях
    line_height = 14

    # Разбиваем текст на строки с учетом максимальной ширины
    lines = text.split('\n')
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(textwrap.wrap(line, width=int(max_width/7)))

    for line in wrapped_lines:
        # Проверка, достаточно ли места на странице для следующей строки
        if text_object.getY() - line_height < 40:  # 40 - нижний отступ страницы
            c.drawText(text_object)
            c.showPage()  # Создание новой страницы
            text_object = c.beginText(40, height - 40)  # Перенос текста на новую страницу
            text_object.setFont("DejaVuSans", 12)

        for text_highlighter in ("Intent:", "Generated characters:", "History of interaction"):
            if text_highlighter in line:
                parts = line.split(text_highlighter)
                text_object.textOut(parts[0])

                x, y = text_object.getX(), text_object.getY()

                intent_width = c.stringWidth(text_highlighter, "DejaVuSans", 12)
                c.setFillColor(colors.yellow)
                c.rect(x, y - 2, intent_width, 14, fill=1)
                c.setFillColor(colors.black)
                text_object.textOut(text_highlighter)
                text_object.textOut(parts[1])

                # Переход на новую строку после выделенного текста
                text_object.textLine("")
                break
        else:
            text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()


async def download_pdf(name_room):
    history = await get_history(name_room)
    text = f'Intent:\n{history[1]}\n\n'
    text += '-'*50
    text += f'\nGenerated characters:\n\n{history[3]}\n'
    text += '-'*50
    text += f'\nHistory of interaction:\n\n{history[2]}'

    file_name = f'output_room_{name_room}.pdf'
    string_to_pdf(text, file_name)

    file_path = os.path.abspath(file_name)
    return file_path, file_name
