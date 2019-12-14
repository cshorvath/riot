import json
import logging
from abc import ABC, abstractmethod
from typing import Iterable, Callable

import paho.mqtt.client as mqtt


class MQTTSubscriber(ABC):
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
    ) -> None:
        self._qos = qos
        self._mqtt_client = mqtt.Client(client_id)
        self._mqtt_client.on_connect = self._get_on_connect_cb(topics, qos)
        self._mqtt_client.on_disconnect = lambda client, userdata, rc: self._on_disconnect(rc)
        self._mqtt_client.on_message = lambda client, userdata, message: self._on_message(message)
        self._mqtt_client.on_publish = lambda client, userdata, mid: self._on_publish(mid)
        self._mqtt_client.connect(mqtt_broker_host, mqtt_broker_port)
        self._subscribers = set()
        self._publish_callbacks = {}

    def start(self):
        return self._mqtt_client.loop_forever()

    def stop(self):
        logging.info(f"{self} stop called")
        self._mqtt_client.disconnect()

    def publish(self, topic, payload, qos=None, cb: Callable[[], None] = None):
        if qos is None:
            qos = self._qos
        logging.debug(f"Publish message to topic[{topic}]")
        msg_info = self._mqtt_client.publish(topic, payload, qos=qos)
        if cb:
            self._publish_callbacks[msg_info.mid] = cb

    def publish_json(self, topic, payload, qos=None, cb: Callable[[], None] = None):
        self.publish(topic, json.dumps(payload), qos, cb)

    def add_subscriber(self, subscriber: MQTTSubscriber):
        self._subscribers.add(subscriber)

    def _get_on_connect_cb(self, topics: Iterable[str], qos: int):
        def callback(client, userdata, flags, rc):
            logging.info("Connected to mqtt broker")
            for topic in topics:
                self._mqtt_client.subscribe(topic, qos)
                logging.info(f"Subscribed to MQTT topic {topic}")

        return callback

    def _on_disconnect(self, rc):
        logging.info(f"{self} disconnected")

    def _on_message(self, message):
        for subscriber in self._subscribers:
            subscriber.on_message(message.topic, message.payload)

    def _on_publish(self, mid):
        try:
            logging.debug(f"Message[{mid}] published")
            self._publish_callbacks[mid]()
        except KeyError:
            logging.error(f"Could not find callback for published message[{mid}]")

    def __del__(self):
        self.stop()
