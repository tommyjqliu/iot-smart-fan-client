import RPi.GPIO as GPIO
from lib.button import Button
from lib.camera import Camera
from lib.fan import Fan
from lib.led import Led
from lib.mqtt import MQTT
import asyncio

from lib.relay import Relay
from lib.utils import await_helper


STOP = asyncio.Event()

class SmartFan():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.running = False
        self.submodule_definition = [
            ("relay", Relay, {}),
            ("led", Led, {}),
            ("button", Button, {}),
            ("fan", Fan, {}),
            ("camera", Camera, {}),
            ("mqtt", MQTT.create, {"on_message": self.on_message})
        ]
        self.submodules = {}
        

    def on_message(self, data):
        print(f'fan received message: {data}', type(data))
        # speed = int(data["speed"])
        # self.setSpeed(speed)
    
    async def turn_on(self):
        for name, cls, params in self.submodule_definition:
            self.submodules[name] = await await_helper(cls(**params))
        self.running = True

    async def turn_off(self):
        self.running = False
        for name, _, _ in self.submodule_definition:
            module = self.submodules.get(name)
            if module:
                await await_helper(module.on_close())


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

