import asyncio
import signal
from smart_fan import SmartFan
import uvloop




if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    smart_fan = SmartFan(loop)

    loop.add_signal_handler(signal.SIGINT, smart_fan.ask_close)
    loop.add_signal_handler(signal.SIGTERM, smart_fan.ask_close)
    loop.run_until_complete(smart_fan.start())