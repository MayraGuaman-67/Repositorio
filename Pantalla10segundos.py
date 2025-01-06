import machine
import time
import ujson
from math import sin, cos, radians
from ST7735 import TFT, TFTColor
from machine import SPI, Pin
from sysfont import sysfont
# Configuración de pines y pantalla
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
tft = TFT(spi, 16, 17, 18)
# Inicialización de la pantalla TFT
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

# Centro de la pantalla
CENTER_X = 64
CENTER_Y = 80
RADIUS = 60
CENTER_X = 64
CENTER_Y = 80
RADIUS = 50

# Posición del reloj digital
DIGITAL_X = 40
DIGITAL_Y = 145

# Archivo para guardar la hora
TIME_FILE = "current_time.json"

def show_intro():
    tft.fill(TFT.BLACK)
    name = "Ayala y Asociados"
    tft.text((15, 90), name, TFT.WHITE, sysfont)  # Muestra el nombre
    draw_logo()  # Dibuja un logo simple
    time.sleep(3)  # Pausa de 3 segundos antes de iniciar el reloj
    clear_text((15, 90), "Ayala y Asociados", sysfont)

def clear_text(position, text, font, background_color=TFT.BLACK):
    """
    Borra el texto mostrado en pantalla dibujando un rectángulo lleno sobre él.
    
    :param position: Tuple con las coordenadas (x, y) del texto.
    :param text: El texto que fue mostrado.
    :param font: La fuente usada para dibujar el texto.
    :param background_color: El color de fondo para "borrar" (por defecto, negro).
    """
    # Calcular el tamaño del área ocupada por el texto
    text_width = len(text) * (font['Width'] + 1)  # Ancho de cada carácter más espacio
    text_height = font['Height']                 # Altura de la fuente

    # Dibujar un rectángulo lleno sobre el área ocupada por el texto
    tft.fillrect(position, (text_width, text_height), background_color)
# Función para dibujar un logo simple
def draw_logo():
    tft.fillcircle((64, 35), 6, TFT.WHITE)  # Cabeza

    # Dibuja el cuerpo (línea)
    tft.line((64, 40), (64, 50), TFT.WHITE)  # Cuerpo

    # Dibuja los brazos (líneas)
    tft.line((64, 45), (54, 50), TFT.WHITE)  # Brazo izquierdo
    tft.line((64, 45), (74, 50), TFT.WHITE)  # Brazo derecho

    # Dibuja las piernas (líneas)
    tft.line((64, 55), (54, 65), TFT.WHITE)  # Pierna izquierda
    tft.line((64, 55), (74, 65), TFT.WHITE)  # Pierna derecha

# Función para guardar la hora inicial en un archivo
def save_time(hours, minutes, seconds):
    with open(TIME_FILE, "w") as f:
        ujson.dump({"hours": hours, "minutes": minutes, "seconds": seconds}, f)

# Función para cargar la hora desde el archivo
def load_time():
    try:
        with open(TIME_FILE, "r") as f:
            data = ujson.load(f)
            return data["hours"], data["minutes"], data["seconds"]
    except (OSError, ValueError, KeyError):
        return None  # Si no existe el archivo o está dañado, devolvemos None

# Función para dibujar las agujas del reloj
def draw_hand(center_x, center_y, length, angle, color):
    end_x = int(center_x + length * cos(radians(angle - 90)))
    end_y = int(center_y + length * sin(radians(angle - 90)))
    tft.line((center_x, center_y), (end_x, end_y), color)

# Función para dibujar la carátula del reloj
def draw_clock_face():
    tft.circle((CENTER_X, CENTER_Y), RADIUS, TFT.GREEN)
    for i in range(12):
        angle = i * 30
        outer_x = int(CENTER_X + RADIUS * cos(radians(angle - 90)))
        outer_y = int(CENTER_Y + RADIUS * sin(radians(angle - 90)))
        inner_x = int(CENTER_X + (RADIUS - 10) * cos(radians(angle - 90)))
        inner_y = int(CENTER_Y + (RADIUS - 10) * sin(radians(angle - 90)))
        tft.line((inner_x, inner_y), (outer_x, outer_y), TFT.WHITE)

# Función para calcular la posición de las agujas
def calculate_angles(hours, minutes, seconds):
    hour_angle = (hours % 12) * 30 + (minutes / 60) * 30
    minute_angle = minutes * 6 + (seconds / 60) * 6
    second_angle = seconds * 6
    return hour_angle, minute_angle, second_angle

# Función para mostrar la hora digital
def draw_digital_clock(hours, minutes, seconds):
    # Formatear la hora
    time_string = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    # Borrar el área previa del reloj digital
    tft.fillrect((DIGITAL_X, DIGITAL_Y), (100, 18), TFT.BLACK)
    # Dibujar el texto con la hora
    tft.text((DIGITAL_X, DIGITAL_Y), time_string, TFT.CYAN, sysfont)

# Función principal
def main():
    show_intro()

    # Cargar la hora inicial desde el archivo o esperar por la computadora
    loaded_time = load_time()
    if loaded_time:
        saved_hours, saved_minutes, saved_seconds = loaded_time
        print("Hora cargada desde el archivo:", saved_hours, saved_minutes, saved_seconds)
    else:
        print("Esperando la hora desde la computadora...")
        import sys
        line = sys.stdin.readline().strip()  # Leer desde la entrada serial
        try:
            saved_hours, saved_minutes, saved_seconds = map(int, line.split(":"))
            save_time(saved_hours, saved_minutes, saved_seconds)
        except:
            print("Error al recibir la hora. Usando 00:00:00.")
            saved_hours, saved_minutes, saved_seconds = 0, 0, 0

    start_time = time.time()

    draw_clock_face()
    while True:
        # Calcular la hora actual basada en el tiempo transcurrido
        elapsed = int(time.time() - start_time)
        current_seconds = (saved_seconds + elapsed) % 60
        current_minutes = (saved_minutes + (saved_seconds + elapsed) // 60) % 60
        current_hours = (saved_hours + (saved_minutes + (saved_seconds + elapsed) // 60) // 60) % 24

        # Calcular ángulos para las agujas
        hour_angle, minute_angle, second_angle = calculate_angles(current_hours, current_minutes, current_seconds)

        # Limpiar el área del reloj analógico y redibujar las agujas
        tft.fillcircle((CENTER_X, CENTER_Y), RADIUS - 2, TFT.BLACK)
        draw_hand(CENTER_X, CENTER_Y, RADIUS - 20, hour_angle, TFT.BLUE)
        draw_hand(CENTER_X, CENTER_Y, RADIUS - 10, minute_angle, TFT.GREEN)
        draw_hand(CENTER_X, CENTER_Y, RADIUS - 5, second_angle, TFT.RED)

        # Dibujar el reloj digital
        draw_digital_clock(current_hours, current_minutes, current_seconds)

        # Guardar la hora actual cada minuto
        if current_seconds == 0:
            save_time(current_hours, current_minutes, current_seconds)
        # Esperar un segundo antes de actualizar
        time.sleep(1)

# Ejecutar el programa principal
main()
