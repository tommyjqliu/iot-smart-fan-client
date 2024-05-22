import RPi.GPIO as GPIO
import asyncio
import time
# Set GPIO Pins
GPIO_TRIGGER = 11
GPIO_ECHO = 26
class Distance:
    def __init__(self, smart_fan, trigger_pin=GPIO_TRIGGER, echo_pin=GPIO_ECHO ,  threshold=10):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.smart_fan = smart_fan
        self.threshold = threshold
        self._running = True
        self.detect_task = asyncio.create_task(self.run())
        self.last_speed = 0
        # Set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    async def distance(self):
        # Set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)

        # Set Trigger after 0.01ms to LOW
        await asyncio.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        StartTime = time.time()
        StopTime = time.time()

        # Save StartTime
        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()

        # Save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()

        # Time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # Multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

    async def run(self):
        await asyncio.sleep(5)
        while True:
            if self._running:
                await self.detect_distance()
            await asyncio.sleep(1)  # Wait for 15 seconds

    async def detect_distance(self):
        dist = await self.distance()
        if dist < self.threshold:
            self.turn_off_fan()
        else:
            self.turn_on_fan()

    def turn_off_fan(self):
        if self.smart_fan.modules["fan"].speed:
            self.last_speed = self.smart_fan.modules["fan"].speed
            self.smart_fan.modules["fan"].speed = 0
            self.smart_fan.modules["led"].run_color_wipe(255, 0, 0)
            print("Fan turned off")

    def turn_on_fan(self):
        if self.last_speed:
            self.smart_fan.modules["fan"].speed = self.last_speed
            self.last_speed = 0
            self.smart_fan.modules["led"].run_color_wipe(0, 0, 255)
            print("Fan turned on")

    def on_close(self):
        self._running = False
        if self.detect_task:
            self.detect_task.cancel()