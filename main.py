import asyncio
import signal
from fan import Fan
from mqtt import MQTT, ask_exit
import RPi.GPIO as GPIO
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def main():
    fan = Fan()
    mqtt = MQTT(fan.message_handler)
    await mqtt.start()
    GPIO.cleanup()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)
    loop.run_until_complete(main())