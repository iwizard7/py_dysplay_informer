import time
import psutil
import socket
from datetime import datetime
from random import randint
from PIL import Image, ImageDraw, ImageFont
from Adafruit_SSD1306 import SSD1306_128_64

# Настройка дисплея
disp = SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

# Функция для получения IP-адреса
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "No IP"

# Функция для получения температуры процессора
def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = int(f.read()) / 1000.0
    return temp

# Настройка шрифта
font = ImageFont.load_default()

# Создание изображений для отрисовки
width = disp.width
height = disp.height

# Основной цикл
start_time = time.time()
while True:
    elapsed_time = time.time() - start_time

    if elapsed_time < 40:  # Основной режим
        # Переключение экранов
        if int(elapsed_time / 10) % 2 == 0:
            # Первый экран: загрузка CPU, память, диск
            image = Image.new("1", (width, height))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), f"CPU Load: {psutil.cpu_percent()}%", font=font, fill=255)
            draw.text((0, 10), f"RAM: {psutil.virtual_memory().percent}%", font=font, fill=255)
            draw.text((0, 20), f"Disk: {psutil.disk_usage('/').percent}%", font=font, fill=255)
        else:
            # Второй экран: IP, температура, время
            image = Image.new("1", (width, height))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), f"IP: {get_ip()}", font=font, fill=255)
            draw.text((0, 10), f"Temp: {get_cpu_temp():.1f} C", font=font, fill=255)
            draw.text((0, 20), f"Time: {datetime.now().strftime('%H:%M:%S')}", font=font, fill=255)
        # Обновление дисплея
        disp.image(image)
        disp.display()
        time.sleep(1)
    else:  # Режим заставки
        for _ in range(50):  # Период заставки
            image = Image.new("1", (width, height))
            draw = ImageDraw.Draw(image)
            # Координаты глаз
            left_eye_x = randint(10, 20)
            left_eye_y = randint(20, 30)
            right_eye_x = randint(70, 80)
            right_eye_y = randint(20, 30)

            # Рисуем глаза
            draw.ellipse((left_eye_x, left_eye_y, left_eye_x + 10, left_eye_y + 10), outline=255, fill=0)
            draw.ellipse((right_eye_x, right_eye_y, right_eye_x + 10, right_eye_y + 10), outline=255, fill=0)

            # Рисуем моргание
            if randint(0, 10) > 8:
                draw.line((left_eye_x, left_eye_y + 5, left_eye_x + 10, left_eye_y + 5), fill=255)
                draw.line((right_eye_x, right_eye_y + 5, right_eye_x + 10, right_eye_y + 5), fill=255)

            disp.image(image)
            disp.display()
            time.sleep(0.1)

        start_time = time.time()  # Перезапуск цикла
