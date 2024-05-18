import requests
import json
import asyncio

URL = "https://iot-smart-fan.vercel.app/api/fan"

class Reporter:
    def __init__(self, smart_fan):
        self.smart_fan = smart_fan
        self.report_task = asyncio.create_task(self.run())


    async def report(self, online = True):
        try:
            data = {
                "online": online,
                "active": self.smart_fan.active,
                "fan_speed": self.smart_fan.modules["fan"].speed,
                "temperature": self.smart_fan.modules["temperature"].target_temperature,
            }

            json_data = json.dumps(data)
            print(json_data)
            self.smart_fan.modules["mqtt"].report(json_data)
            response = requests.post(URL, data=json_data, headers={'Content-Type': 'application/json'})

            if response.status_code == 200:
                print("Data sent successfully!")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"An error occurred during report: {e}")

    async def run(self):
        await asyncio.sleep(5)
        while True:
            await self.report()
            await asyncio.sleep(15)  # Wait for 15 seconds
    
    async def on_close(self):
        await self.report(False)
        self.report_task.cancel()