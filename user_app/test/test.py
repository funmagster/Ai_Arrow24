import pygame
import pyaudio
import wave
import speech_recognition as sr
import threading
import time

# Инициализация Pygame
pygame.init()

# Размеры окна и иконка микрофона
window_size = (400, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Voice Recorder")
microphone_icon = pygame.image.load(
    r"C:\Users\kulib\PycharmProjects\Ai_Arrow24\admin_app\img\microphone.png")  # Замените на путь к вашей иконке микрофона
icon_rect = microphone_icon.get_rect(center=(window_size[0] // 2, window_size[1] // 2))

# Настройки записи
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
stream = None
frames = []
recording = False


def start_recording():
    global stream, frames, recording
    frames = []
    recording = True
    # Инициализация нового потока записи
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("Recording started...")

    def record():
        while recording:
            data = stream.read(CHUNK)
            frames.append(data)

    threading.Thread(target=record).start()


def stop_recording():
    global stream, frames, recording, p
    if stream:
        recording = False
        stream.stop_stream()
        stream.close()
        # Оставляем `p` и не вызываем `p.terminate()` здесь

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("Recording stopped and saved to", WAVE_OUTPUT_FILENAME)

        recognize_speech()

        # Восстановление состояния потока
        p.terminate()
        p = pyaudio.PyAudio()
        stream = None  # Убедитесь, что `stream` сброшен


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            print("You said:", text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if icon_rect.collidepoint(event.pos):
                start_recording()
        elif event.type == pygame.MOUSEBUTTONUP:
            if icon_rect.collidepoint(event.pos) and recording:
                stop_recording()

    screen.fill((255, 255, 255))
    screen.blit(microphone_icon, icon_rect)
    pygame.display.flip()

pygame.quit()
