import asyncio
import gmqtt
import json

HOST = 'broker.hivemq.com'
CLIENT_ID = "CITS5506SMARTFAN_CLIENT"

class MQTT:
    def __init__(self, on_message, broker_host = HOST, client_id=CLIENT_ID):
        self.client = gmqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.on_disconnect = self.on_disconnect
        # self.client.on_subscribe = self.on_subscribe
        self.on_message_callback = on_message
        self.broker_host = broker_host
        asyncio.create_task(self.client.connect(self.broker_host))

    def on_connect(self, client, flags, rc, properties):
        self.client.subscribe('CITS5506SMARTFAN/CONTROL', qos=1)

    def on_message(self, client, topic, payload, qos, properties):
        self.on_message_callback(data = json.loads(payload))

    # def on_disconnect(self, client, packet, exc=None):
    #     print('Disconnected')

    # def on_subscribe(self, client, mid, qos, properties):
    #     print('SUBSCRIBED')

    def report(self, data):
        self.client.publish("CITS5506SMARTFAN/REPORT", data)
    
    async def on_close(self):
        await self.client.disconnect()


