import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from json import JSONDecodeError
from typing import Iterable

import paho.mqtt.client as mqtt

from common.model.model import MessageDirection
from message_processor.db.db_persister import DBPersister


class AMQTTObserver(ABC):

    def __init__(
            self,
            mqtt_client: mqtt.Client,
            topics: Iterable[str],
            mqtt_broker_host: str,
            mqtt_broker_port: int = 1883,
            qos: int = 1
    ) -> None:
        self._mqtt_host = mqtt_broker_host
        self._mqtt_port = mqtt_broker_port
        self._mqtt_client = mqtt_client
        self._topics = topics
        self._qos = qos
        self._started = False

        self._mqtt_client.on_connect = lambda client, userdata, flags, rc: self._on_connect(rc)
        self._mqtt_client.on_disconnect = lambda client, userdata, rc: self._on_disconnect(rc)
        self._mqtt_client.on_message = lambda c, u, m: self._on_message(c, u, m)

    def start(self):
        assert not self._started, self.__class__.__name__ + " already started"
        self._mqtt_client.connect(self._mqtt_host, self._mqtt_port)
        self._started = True
        return self._mqtt_client.loop_forever()

    def stop(self):
        logging.info(f"{self} stop called")
        self._mqtt_client.disconnect()

    def _on_connect(self, rc):
        logging.info(f"Connected to mqtt broker [{self._mqtt_host}:{self._mqtt_port}], result code: [{rc}]")
        for topic in self._topics:
            self._mqtt_client.subscribe(topic)

    def _on_disconnect(self, rc):
        logging.info(f"{self} disconnected")

    @abstractmethod
    def _on_message(self, client, userdata, message):
        pass

    def __del__(self):
        self.stop()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self._mqtt_host}:{self._mqtt_port}]"


class DataObserver(AMQTTObserver):

    def __init__(
            self,
            db_persister: DBPersister,
            topics: Iterable[str],
            mqtt_broker_host: str,
            mqtt_broker_port: int = 1883,
            qos: int = 1,
            mqtt_client: mqtt.Client = None,
            device_id_idx=2
    ) -> None:
        super(DataObserver, self).__init__(
            mqtt_client or mqtt.Client("riot_message_processor"),
            topics,
            mqtt_broker_host,
            mqtt_broker_port,
            qos
        )
        self._db_persister = db_persister
        self._device_id_idx = device_id_idx

    def _on_message(self, client, userdata, message):
        device_id = self.parse_device_id(message.topic)
        logging.info(f"Message arrived from device[{device_id}]")
        try:
            msg_dict = json.loads(message.payload)
        except JSONDecodeError as e:
            logging.error(f"Error decoding message from topic [{message.topic}], payload: [{message.payload}]")
            return

        timestamp: int = msg_dict.get("timestamp", 0)
        payload: dict = msg_dict.get("payload", None)
        self._db_persister.store_message(
            device_id,
            MessageDirection.INBOUND,
            datetime.fromtimestamp(timestamp / 1000),
            json.dumps(payload)
        )

    def parse_device_id(self, topic_name: str):
        """
        Parses device id from topic name. Topic name expected to consist of parts separated with "/"
        :param topic_name:
        :return: device id
        """
        topic_splitted = topic_name.split("/")
        if len(topic_splitted) >= self._device_id_idx + 1:
            device_id_str = topic_splitted[self._device_id_idx]
            if device_id_str.isdigit():
                return int(device_id_str)
        logging.error(f"Unable to parse device_id from topic name: {topic_name}")
        return -1
