import RPi.GPIO as GPIO
import asyncio
from lib import Button, Camera, Fan, Led, MQTT, Temperature, await_helper


STOP = asyncio.Event()

class SmartFan():
    def __init__(self, loop):
        GPIO.setmode(GPIO.BCM)
        self.loop = loop
        self.running = False
        self.module_definition = [
            ("fan", Fan, {}),
            ("led", Led, {}),
            # ("button", Button, {"loop": loop, "callback": self.on_button}),
            # ("camera", Camera, {}),
            # ("temperature", Temperature, {}),
            ("mqtt", MQTT.create, {"on_message": self.on_message})
        ]
        self.modules = {}
        

    def on_message(self, data):
        print(f'fan received message: {data}', type(data))
        # speed = int(data["speed"])
        # self.setSpeed(speed)

    def on_button(self, event, time):
        print(event)

    async def turn_on(self):
        gathers = []
        for name, cls, params in self.module_definition:
            gathers.append(await_helper(cls(**params)))
        instances = await asyncio.gather(*gathers)
        for i, (name, cls, params),  in enumerate(self.module_definition):
            self.modules[name] = instances[i]
        self.running = True

    async def turn_off(self):
        self.running = False
        gathers = []
        for name, _, _ in self.module_definition:
            module = self.modules.get(name)
            if module:
               gathers.append(await_helper(module.on_close()))
        
        try:
            await asyncio.gather(*gathers)
        except Exception as e:
            print(f"An error occurred during close: {e}")

    ### Life Cycle ###

    async def start(self):
        try:
            await self.turn_on()
            self.modules['fan'].speed = 50
            await STOP.wait()
        except Exception as e:
            print(f"An error occurred during operation: {e}")
        finally:
            await self.on_close()

    def ask_close(self):
        STOP.set()
    
    async def on_close(self):
        await self.turn_off()

