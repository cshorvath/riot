import logging
from abc import ABC, abstractmethod
from typing import Iterable

import paho.mqtt.client as mqtt


class MQTTObserver(ABC):
    @abstractmethod
    def on_message(self, topic: str, payload: str):
        pass


class MQTTClientWrapper:
    def __init__(
            self,
            client_id: str,
            mqtt_broker_host: str,
            mqtt_broker_port: int,
            topics: Iterable[str],
            qos: int,
            observer: MQTTObserver = None
    ) -> None:
        self._qos = qos
        self._mqtt_client = mqtt.Client(client_id)
        self._mqtt_client.enable_logger()
        self._mqtt_client.on_connect = self._get_on_connect_cb(topics, qos)
        self._mqtt_client.on_disconnect = lambda client, userdata, rc: self._on_disconnect(rc)
        self._mqtt_client.on_message = lambda client, userdata, message: self._on_message(message)
        self._mqtt_client.connect(mqtt_broker_host, mqtt_broker_port)
        self.observer = observer

    def start(self):
        return self._mqtt_client.loop_forever()

    def stop(self):
        logging.info(f"{self} stop called")
        self._mqtt_client.disconnect()

    def publish(self, topic, payload, qos=None):
        if qos is None:
            qos = self._qos
        self._mqtt_client.publish(topic, payload, qos=qos)

    def _get_on_connect_cb(self, topics: Iterable[str], qos: int):
        def callback(client, userdata, flags, rc):
            logging.info(f"Connected to mqtt broker")
            for topic in topics:
                self._mqtt_client.subscribe(topic, qos)
                logging.info(f"Subscribed to MQTT topic {topic}")

        return callback

    def _on_disconnect(self, rc):
        logging.info(f"{self} disconnected")

    def _on_message(self, message):
        self.observer.on_message(message.topic, message.payload)

    def __del__(self):
        self.stop()
