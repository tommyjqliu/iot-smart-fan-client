import RPi.GPIO as GPIO
from gpiozero import Button as GPIOButton

GPIO_BUTTON = 19

class Button():
    def __init__(self, pin=GPIO_BUTTON , on_press=None, on_release=None):
        self.button = GPIOButton(pin)
        self.press_callback = on_press
        self.release_callback = on_release

        # Attach the callback functions to the button events
        if self.press_callback:
            self.button.when_pressed = self.press_callback
        if self.release_callback:
            self.button.when_released = self.release_callback
    
    def on_close(self):
        GPIO.cleanup()
