import json
import RPi.GPIO as GPIO
from led import Led

PWM_GPIO = 12
RELAIS_GPIO = 17
LED_GPIO = 18

class Fan():
    def hardware_setup(self):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM_GPIO, GPIO.OUT)
        self.pwm = GPIO.PWM(PWM_GPIO, 1000)
        self.pwm.start(0)
        
        GPIO.setup(RELAIS_GPIO, GPIO.OUT)
        GPIO.output(RELAIS_GPIO, GPIO.LOW)

        self.led = Led(LED_GPIO)

    def __init__(self):
        
        self.speed = 0
        self.hardware_setup()

    def message_handler(self, data_str):
        data = json.loads(data_str)
        print(f'fan received message: {data}', type(data))
        speed = int(data["speed"])
        self.setSpeed(speed)
        
    def register(self):
        print(f'{self.id} fan is registered')

    def setSpeed(self, speed):
        if speed == 0:
            print(22)
            GPIO.output(RELAIS_GPIO, GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)
        else:
            GPIO.output(RELAIS_GPIO, GPIO.HIGH)
            print(f"change{min(speed, 100)}")
            self.pwm.ChangeDutyCycle(min(speed, 100))

