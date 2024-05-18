import RPi.GPIO as GPIO
import asyncio
from lib import Button, Camera, Fan, Led, MQTT, Relay, Temperature, await_helper


STOP = asyncio.Event()

class SmartFan():
    def __init__(self, loop):
        GPIO.setmode(GPIO.BCM)
        self.loop = loop
        self.running = False
        self.submodule_definition = [
            ("relay", Relay, {}),
            ("fan", Fan, {}),
            ("led", Led, {}),
            # ("button", Button, {"loop": loop, "callback": self.on_button}),
            # ("camera", Camera, {}),
            # ("temperature", Temperature, {}),
            ("mqtt", MQTT.create, {"on_message": self.on_message})
        ]
        self.submodules = {}
        

    def on_message(self, data):
        print(f'fan received message: {data}', type(data))
        # speed = int(data["speed"])
        # self.setSpeed(speed)

    def on_button(self, event, time):
        print(event)

    async def turn_on(self):
        for name, cls, params in self.submodule_definition:
            self.submodules[name] = await await_helper(cls(**params))
        self.running = True

    async def turn_off(self):
        self.running = False
        for name, _, _ in self.submodule_definition:
            module = self.submodules.get(name)
            if module:
                try:
                    await await_helper(module.on_close())
                except Exception as e:
                    print(f"An error occurred during close: {e}")


    ### Life Cycle ###

    async def start(self):
        try:
            await self.turn_on()
            await STOP.wait()
        except Exception as e:
            print(f"An error occurred during operation: {e}")
        finally:
            await self.on_close()

    def ask_close(self):
        STOP.set()
    
    async def on_close(self):
        await self.turn_off()

