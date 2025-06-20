import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Esperando pulsaciones en el botón conectado a GPIO27 (pin físico 13)...")

try:
    while True:
        if GPIO.input(27) == GPIO.LOW:
            print("¡Botón pulsado!")
            time.sleep(0.3)
except KeyboardInterrupt:
    GPIO.cleanup()
