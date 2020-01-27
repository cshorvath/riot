import json
import os
from sys import argv

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, message: mqtt.MQTTMessage):
    pass


DEVICE_ID = argv[1]

topic = f"riot/device/{DEVICE_ID}/outgoing"
mqtt_broker = os.getenv("MQTT_HOST", "localhost")
client = mqtt.Client("DummyClient", clean_session=False)
client.connect(mqtt_broker, 1883, 60)
client.loop_start()
while True:
    try:
        value = float(input("Value: "))
        msg_info = client.publish(
            topic=topic,
            payload=json.dumps({"payload": {
                "value": value,
            }
            }),
            qos=2
        )
        msg_info.wait_for_publish()
    except ValueError:
        continue
