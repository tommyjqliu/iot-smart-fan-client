import asyncio
import signal
from lib.smart_fan import SmartFan
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

smart_fan = SmartFan()

async def main():
    await smart_fan.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, smart_fan.ask_close)
    loop.add_signal_handler(signal.SIGTERM, smart_fan.ask_close)
    loop.run_until_complete(main())