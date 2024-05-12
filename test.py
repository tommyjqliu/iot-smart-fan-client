import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 1000)
p.start(0)

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = 17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode


time.sleep(2)

try:
    while True:
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
        p.ChangeDutyCycle(100)
        print('100')
        time.sleep(5)
        p.ChangeDutyCycle(50)
        print('50')
        time.sleep(5)
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
        p.ChangeDutyCycle(0)
        print('0')
        time.sleep(5)
            
except KeyboardInterrupt:
    pass

p.ChangeDutyCycle(0)
p.stop()
GPIO.cleanup()
