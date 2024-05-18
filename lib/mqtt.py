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
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.on_message_callback = on_message
        self.broker_host = broker_host
        
    @classmethod
    async def create(cls, on_message, broker_host = HOST, client_id=CLIENT_ID):
        mqtt = cls(on_message, broker_host, client_id)
        await mqtt.client.connect(mqtt.broker_host)
        return mqtt

    def on_connect(self, client, flags, rc, properties):
        print('Connected')
        client.subscribe('CITS5506SMARTFAN/#', qos=0)

    def on_message(self, client, topic, payload, qos, properties):
        self.on_message_callback(data = json.loads(payload))

    def on_disconnect(self, client, packet, exc=None):
        print('Disconnected')

    def on_subscribe(self, client, mid, qos, properties):
        print('SUBSCRIBED')

    async def on_close(self):
        await self.client.disconnect()


