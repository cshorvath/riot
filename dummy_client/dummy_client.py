import datetime
import json
import os
from sys import argv
from time import sleep

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, message: mqtt.MQTTMessage):
    print(client, userdata, message.payload, message.qos)


topic = "riot/device/1"
client_type = argv[1]

mqtt_broker = os.getenv("MQTT_HOST", "localhost")
client = mqtt.Client("DummyClient_" + client_type, clean_session=False)
client.connect(mqtt_broker, 1883, 60)
c = 0

if client_type == "sub":
    print("Sub mode")
    client.subscribe(
        topic=topic,
        qos=2
    )
    client.on_message = on_message
    client.loop_forever()

client.on_publish = lambda client, userdata, mid: print(mid)
while True:
    msg_info = client.publish(
        topic=topic,
        payload=json.dumps({"timestamp": datetime.datetime.now().timestamp() * 1000, "payload": {"x": c}}),
        qos=2
    )
    c += 1
    sleep(0.5)
    client.loop(1, 100)
