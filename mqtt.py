import asyncio
import time
import gmqtt

STOP = asyncio.Event()

HOST = 'broker.hivemq.com'
CLIENT_ID = "CITS5506SMARTFAN_CLIENT"

class MQTT:
    def __init__(self, on_message_callback, broker_host = HOST, client_id=CLIENT_ID):
        self.client = gmqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.on_message_callback = on_message_callback
        self.broker_host = broker_host

    def on_connect(self, client, flags, rc, properties):
        print('Connected')
        client.subscribe('CITS5506SMARTFAN/#', qos=0)

    def on_message(self, client, topic, payload, qos, properties):
        self.on_message_callback(payload)

    def on_disconnect(self, client, packet, exc=None):
        print('Disconnected')

    def on_subscribe(self, client, mid, qos, properties):
        print('SUBSCRIBED')

    async def start(self):
        await self.client.connect(self.broker_host)
        self.client.publish('TEST/TIME', str(time.time()), qos=1)
        await STOP.wait()
        await self.client.disconnect()


def ask_exit(*args):
    STOP.set()


