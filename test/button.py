
import time
from gpiozero import Button as GPIOButton
from threading import Timer

GPIO_BUTTON = 19

class Button():
    def __init__(self, pin=GPIO_BUTTON, on_click=None, on_double_click=None, on_hold=None):
        self.button = GPIOButton(pin)
        self.click_callback = on_click
        self.double_click_callback = on_double_click
        self.hold_callback = on_hold

        self.last_press_time = 0
        self.press_count = 0
        self.click_timer = None
        self.hold_timer = None

        # Constants for timing
        self.debounce = 0.05  # debounce time to avoid detecting false double clicks
        self.double_click_max_gap = 0.3  # max time between clicks for a double click
        self.hold_time = 1.0  # time to consider the button press as a hold

        # Attach event handlers
        self.button.when_pressed = self.handle_press
        self.button.when_released = self.handle_release

    def handle_press(self):
        current_time = time.time()
        if (current_time - self.last_press_time) > self.debounce:
            self.press_count += 1
        self.last_press_time = current_time

        if self.hold_timer is not None:
            self.hold_timer.cancel()
        self.hold_timer = Timer(self.hold_time, self.trigger_hold)
        self.hold_timer.start()

    def handle_release(self):
        if self.hold_timer is not None:
            self.hold_timer.cancel()

        if self.press_count == 1:
            if self.click_timer is not None:
                self.click_timer.cancel()
            self.click_timer = Timer(self.double_click_max_gap, self.trigger_click)
            self.click_timer.start()
        elif self.press_count == 2:
            self.trigger_double_click()

    def trigger_click(self):
        if self.press_count == 1 and not self.hold_timer.is_alive():  # Ensure no hold was detected
            if self.click_callback:
                self.click_callback()
        self.reset()

    def trigger_double_click(self):
        if self.double_click_callback:
            self.double_click_callback()
        self.reset()

    def trigger_hold(self):
        if self.hold_callback:
            self.hold_callback()
        self.reset()

    def reset(self):
        self.press_count = 0
        if self.click_timer:
            self.click_timer.cancel()
        if self.hold_timer:
            self.hold_timer.cancel()

    def on_close(self):
        self.button.close()


import time

# Define callback functions for testing
def on_click():
    print("Single click detected")

def on_double_click():
    print("Double click detected")

def on_hold():
    print("Hold detected")

# Create a Button instance with the testing callbacks
test_button = Button(on_click=on_click, on_double_click=on_double_click, on_hold=on_hold)

# Simulated button presses and releases for testing
def simulate_single_click():
    test_button.handle_press()
    time.sleep(0.1)  # Short delay to simulate release time
    test_button.handle_release()

def simulate_double_click():
    test_button.handle_press()
    time.sleep(0.1)  # Short delay to simulate release time
    test_button.handle_release()
    time.sleep(0.2)  # Delay between clicks
    test_button.handle_press()
    time.sleep(0.1)  # Short delay to simulate release time
    test_button.handle_release()

def simulate_hold():
    test_button.handle_press()
    time.sleep(1.2)  # Longer than hold time to trigger hold
    test_button.handle_release()

# Running the tests
print("Testing Single Click:")
simulate_single_click()
time.sleep(1)  # Wait for any delayed reactions

print("Testing Double Click:")
simulate_double_click()
time.sleep(1)  # Wait for any delayed reactions

print("Testing Hold:")
simulate_hold()
time.sleep(1)  # Wait for any delayed reactions

# Properly close the button when done testing
test_button.on_close()
