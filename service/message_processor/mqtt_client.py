import json
from datetime import datetime

import paho.mqtt.client as mqtt

from common.model.model import MessageDirection
from message_processor.db.db_persister import DBPersister


class DataObserver:

    def __init__(self, mqtt_client: mqtt.Client, db_persister: DBPersister) -> None:
        self._mqtt_client = mqtt_client
        self._db_persister = db_persister

    def start(self, topic_pattern: str, mqtt_broker_host: str, mqtt_broker_port: int = 1883, qos=1): # TODO check alreadystarted etc.
        self._mqtt_client.connect(
            host=mqtt_broker_host,
            port=mqtt_broker_port
        )
        self._mqtt_client.subscribe(topic_pattern, qos=qos)
        self._mqtt_client.on_message = lambda client, userdata, message: self._process_message(message)

    def step(self):
        self._mqtt_client.loop()

    def _process_message(self, message: mqtt.MQTTMessage):
        device_id = self.parse_device_id(message.topic)
        msg_dict = json.loads(message.payload)  # todo error handling
        timestamp: int = msg_dict.get("timestamp", 0)
        payload: dict = msg_dict.get("payload", None)
        self._db_persister.store_message(
            device_id,
            MessageDirection.INBOUND,
            datetime.fromtimestamp(timestamp / 1000),
            json.dumps(payload)
        )

    @staticmethod
    def parse_device_id(topic_name: str):
        return int(topic_name.split("/")[2])  # todo error handling
