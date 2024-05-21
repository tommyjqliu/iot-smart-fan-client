import RPi.GPIO as GPIO
import asyncio
from lib import Button, Camera, Fan, Led, MQTT, Temperature, Reporter, await_helper


STOP = asyncio.Event()

class SmartFan():
    def __init__(self, loop):
        GPIO.setmode(GPIO.BCM)
        self.loop = loop
        self.active = False
        self.module_definition = [
            ("fan", Fan, {}),
            ("led", Led, {}),
            ("button", Button, {"loop": loop, "callback": self.on_button}),
            ("camera", Camera, {"smart_fan": self}),
            ("temperature", Temperature, {}),
            ("reporter", Reporter, {"smart_fan": self}),
            ("mqtt", MQTT, {"on_message": self.on_message}),
        ]
        self.modules = {}
        

    def on_message(self, data):
        print(f'Fan received message: {data}')
        self.active = data.get("active", self.active)
        if self.active:
            self.modules["led"].run_color_wipe(0,0,255)
            self.modules["fan"].speed = data.get("fan_speed",self.modules["fan"].speed)
            self.modules["camera"].active = data.get("auto_fan_off",self.modules["camera"].active)
        else:
            self.modules["led"].run_color_wipe(0,0,0)
            self.modules["fan"].speed = 0
            self.modules["camera"].active = False
            

    def on_button(self, event, time):
        print(event)

    async def turn_on(self):
        gathers = []
        for name, cls, params in self.module_definition:
            gathers.append(await_helper(cls(**params)))
        instances = await asyncio.gather(*gathers)
        for i, (name, cls, params),  in enumerate(self.module_definition):
            self.modules[name] = instances[i]
        self.active = True

    async def turn_off(self):
        self.active = False
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

