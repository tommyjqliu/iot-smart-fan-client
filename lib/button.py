from gpiozero import Button as GPIOButton
from threading import Lock, Timer
import time

BUTTON_PIN = 19

class Button(GPIOButton):  # Inherit from GPIOButton
    HOLD_TIMEOUT = 1.5
    CLICK_AND_HOLD_TIMEOUT = 1.5
    DOUBLE_CLICK_TIMEOUT = 0.35
    TRIPLE_CLICK_TIMEOUT = 0.35

    def __init__(self, loop, callback):
        self.button_sequence = 0
        self.button_timer = None
        self.button_sequence_lock = Lock()
        self.button_state = "up"

        super().__init__(pin=BUTTON_PIN, bounce_time=0.05)  # Initialize the GPIOButton

        self.when_pressed = self._handle_press
        self.when_released = self._handle_release
        self.callback = (loop, callback)
    #
    # (0) -- down -> (1) -- timer -> hold
    #                 |
    #                 -- up -> (2) -- timer -> click + goto state 0
    #                           |
    #  _________________________|
    #  |
    #  -- down -> (3) -- timer -> click_and_hold
    #              |
    #              -- up -> (4) -- timer -> double click
    #                        |
    #                        -- down -> (5) -- timer -> click_and_hold
    #
    def _handle_press(self):
        now = time.time()
        with self.button_sequence_lock:
            if self.button_sequence == 0:
                self.button_sequence = 1
                self.button_timer = Timer(self.HOLD_TIMEOUT, self._hold_cb)
                self.button_timer.start()
            elif self.button_sequence == 2:
                self.button_sequence = 3
                self.button_timer = Timer(self.CLICK_AND_HOLD_TIMEOUT, self._click_and_hold_cb)
                self.button_timer.start()
            elif self.button_sequence == 4:
                self.button_sequence = 5
                self.button_timer = Timer(self.TRIPLE_CLICK_TIMEOUT, self._click_and_hold_cb)
                self.button_timer.start()
        self._trigger_event("down", now)

    def _handle_release(self):
        now = time.time()
        if self.button_timer:
            self.button_timer.cancel()
            self.button_timer = None
        with self.button_sequence_lock:
            if self.button_sequence == 1:
                self.button_sequence = 2
                self.button_timer = Timer(self.DOUBLE_CLICK_TIMEOUT, self._click_cb)
                self.button_timer.start()
            elif self.button_sequence == 3:
                self.button_sequence = 4
                self.button_timer = Timer(self.TRIPLE_CLICK_TIMEOUT, self._double_click_cb)
                self.button_timer.start()
            elif self.button_sequence == 5:
                self.button_sequence = 0
                self._trigger_event("triple_click", now)
        self._trigger_event("up", now)

    def _hold_cb(self):
        self._timer_event_cb("hold")

    def _click_and_hold_cb(self):
        self._timer_event_cb("click_and_hold")

    def _click_cb(self):
        self._timer_event_cb("click")

    def _double_click_cb(self):
        self._timer_event_cb("double_click")

    def _timer_event_cb(self, event):
        now = time.time()
        self.button_timer = None
        self.button_sequence = 0
        self._trigger_event(event, now)

    def _trigger_event(self, event, time_stamp):
        if self.callback:
            (loop, callback) = self.callback
            loop.call_soon_threadsafe(lambda: callback(event, time_stamp))
    
    def on_close(self):
        pass
        