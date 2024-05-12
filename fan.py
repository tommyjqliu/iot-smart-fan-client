import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 1000)
p.start(0)
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = 17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.LOW)

class Fan():
    def __init__(self, id):
        self.id = id

    def message_handler(self, data_str):
        data = json.loads(data_str)
        print(f'{self.id} fan received message: {data}', type(data))
        speed = int(data["speed"])
        self.setSpeed(speed)
        
    def register(self):
        print(f'{self.id} fan is registered')

    def setSpeed(self, speed):
        if speed == 0:
            print(22)
            GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
            p.ChangeDutyCycle(0)
        else:
            GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
            print(f"change{min(speed, 100)}")
            p.ChangeDutyCycle(min(speed, 100))

