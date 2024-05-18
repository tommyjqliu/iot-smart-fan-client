import RPi.GPIO as GPIO

from lib.relay import Relay

PWM_GPIO = 12

class Fan:
    def __init__(self):
        GPIO.setup(PWM_GPIO, GPIO.OUT)
        self.pwm = GPIO.PWM(PWM_GPIO, 1000)
        self.pwm.start(0)
        self.relay = Relay()
    
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, _value):
        value = max(0, min(_value, 100))
        if value == 0:
            self.relay.off()
            self.pwm.ChangeDutyCycle(0)
        else:
            self.relay.on()
            self.pwm.ChangeDutyCycle(value)
    
    def on_close(self):
        self.pwm.stop()
        GPIO.cleanup()