import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, tzinfo
from json import JSONDecodeError
from typing import List

import pytz

from core.model.model import MessageDirection
from message_processor.mqtt import parse_device_id
from message_processor.mqtt.mqtt_wrapper import MQTTObserver


@dataclass
class DeviceMessage:
    device_id: int
    timestamp: datetime
    payload: dict
    direction: MessageDirection


class DeviceMessageListener(ABC):
    @abstractmethod
    def on_device_message(self, message: DeviceMessage):
        pass


class DataObserver(MQTTObserver):

    def __init__(self, device_id_idx=2, tz: tzinfo = pytz.utc) -> None:
        self._device_id_idx = device_id_idx
        self._message_listeners: List[DeviceMessageListener] = []
        self._tz = tz

    def add_listener(self, message_listener: DeviceMessageListener):
        self._message_listeners.append(message_listener)

    def on_message(self, topic, payload):
        device_id = parse_device_id(topic)
        logging.info(f"Message arrived from device[{device_id}]")
        try:
            msg_dict = json.loads(payload)
        except JSONDecodeError as e:
            logging.error(
                f"Error decoding message from topic [{topic}], payload: [{payload}], error[{e}]", )
            return

        timestamp: int = msg_dict.get("timestamp", 0) / 1000
        payload: dict = msg_dict.get("payload", None)
        for message_listener in self._message_listeners:
            try:
                message_listener.on_device_message(
                    message=DeviceMessage(
                        device_id=device_id,
                        timestamp=datetime.fromtimestamp(timestamp, tz=self._tz),
                        payload=payload,
                        direction=MessageDirection.INBOUND
                    ),
                )
            except Exception as e:
                logging.exception(e)
                raise
