import RPi.GPIO as GPIO

RELAY_GPIO = 17

class Relay:
    def __init__(self):
        GPIO.setup(RELAY_GPIO, GPIO.OUT)
        GPIO.output(RELAY_GPIO, GPIO.LOW)
    
    def on(self):
        GPIO.output(RELAY_GPIO, GPIO.HIGH)
    
    def off(self):
        GPIO.output(RELAY_GPIO, GPIO.LOW)
    
    def on_close(self):
        GPIO.cleanup()