import datetime
import json
import os
import random
from sys import argv
from time import sleep

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, message: mqtt.MQTTMessage):
    print(client, userdata, message.payload, message.qos)


DEVICE_ID = 101

topic = f"riot/device/{DEVICE_ID}/outgoing"
limit = int(argv[1])

mqtt_broker = os.getenv("MQTT_HOST", "localhost")
client = mqtt.Client("DummyClient", clean_session=False)
client.connect(mqtt_broker, 1883, 60)
c = 0
dt = datetime.datetime(2019, 11, 18, 10, 10, 00)
client.on_publish = lambda client, userdata, mid: print(mid)
while True:
    msg_info = client.publish(
        topic=topic,
        payload=json.dumps({"timestamp": dt.timestamp() * 1000,
                            "payload": {
                                "temperature": random.randint(20, 40),
                                "humidity": random.randint(50, 100)
                            }
                            }),
        qos=2
    )
    c += 1
    dt += datetime.timedelta(minutes=1)
    sleep(0.1)
    client.loop(1, 100)
