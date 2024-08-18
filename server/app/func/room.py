from app.db.db import get_history
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def string_to_pdf(text, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    text_object = c.beginText(40, height - 40)
    text_object.setFont("Helvetica", 12)

    # Разбиваем текст по строкам
    lines = text.split('\n')

    for line in lines:
        text_object.textLine(line)
        # Если нужно добавлять пустые строки, чтобы было больше места между строками
        # text_object.moveCursor(0, -14)  # Настройка значение для увеличения интервала между строками

    c.drawText(text_object)
    c.showPage()
    c.save()


async def download_pdf(name_room):
    history = await get_history(name_room)
    text = f'Изначальный замысел:\nhistory{history[1]}\n\n'
    text += '84'*100
    text += f'Сгенерированные перснонажи:\n{history[3]}\n'
    text += '84' * 100
    text += f'История взаимодействия:\n{history[2]}'

    file_name = f'output_room_{name_room}.pdf'
    string_to_pdf(text, file_name)

    file_path = os.path.abspath(file_name)
    return file_path, file_name
