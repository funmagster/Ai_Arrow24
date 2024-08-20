from app.db.db import get_history
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import textwrap
import os


def string_to_pdf(text, pdf_file):
    """
    Forms a pdf file from the passed string
    :param text: text to generate a pdf file
    :param pdf_file: path to the pdf file to be generated
    :return: None (creates a pdf file)
    """
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Registering a font that supports Cyrillic alphabet
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    text_object = c.beginText(40, height - 40)
    text_object.setFont("DejaVuSans", 12)

    # Set the maximum width of the text
    max_width = width - 80  # Leave indents around the edges

    # Row height in pixels
    line_height = 14

    # Split the text into lines taking into account the maximum width
    lines = text.split('\n')
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(textwrap.wrap(line, width=int(max_width/7)))

    for line in wrapped_lines:
        # Check if there is enough space on the page for the next line
        if text_object.getY() - line_height < 40:  # 40 - page footer
            c.drawText(text_object)
            c.showPage()  # Creating a new page
            text_object = c.beginText(40, height - 40)  # Transferring text to a new page
            text_object.setFont("DejaVuSans", 12)

        for text_highlighter in ("Замысел:", "Сгенерированные персонажи:", "История взаимодействия"):
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

                # Move to a new line after selected text
                text_object.textLine("")
                break
        else:
            text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()


async def download_pdf(name_room):
    history = await get_history(name_room)
    text = f'Замысел:\n{history[1]}\n\n'
    text += '-'*50
    text += f'\nСгенерированные персонажи:\n\n{history[3]}\n'
    text += '-'*50
    text += f'\nИстория взаимодействия:\n\n{history[2]}'

    file_name = f'output_room_{name_room}.pdf'
    string_to_pdf(text, file_name)

    file_path = os.path.abspath(file_name)
    return file_path, file_name
