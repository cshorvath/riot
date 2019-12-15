import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, tzinfo
from json import JSONDecodeError
from typing import Set

import pytz

from data_processor.mqtt.mqtt_wrapper import MQTTSubscriber
from data_processor.util import epochmillis_to_datetime, datetime_to_epochmillis, parse_device_id


@dataclass
class DeviceMessage:
    device_id: int
    timestamp: datetime
    payload: dict

    def to_json(self):
        c = self.__dict__.copy()
        c["timestamp"] = datetime_to_epochmillis(self.timestamp)
        return c


class DeviceMessageListener(ABC):
    @abstractmethod
    def on_device_message(self, message: DeviceMessage):
        pass


class DataObserver(MQTTSubscriber):

    def __init__(self, device_id_idx=2, tz: tzinfo = pytz.utc) -> None:
        self._device_id_idx = device_id_idx
        self._message_listeners: Set[DeviceMessageListener] = set()
        self._tz = tz

    def add_listener(self, message_listener: DeviceMessageListener):
        self._message_listeners.add(message_listener)

    def on_message(self, topic, payload):
        device_id = parse_device_id(topic)
        logging.info(f"Message arrived from device[{device_id}]")
        try:
            msg_dict = json.loads(payload)
        except JSONDecodeError as e:
            logging.error(
                f"Error decoding message from topic [{topic}], payload: [{payload}], error[{e}]", )
            return

        timestamp_millis: int = msg_dict.get("timestamp", None)
        payload: dict = msg_dict.get("payload", None)
        for message_listener in self._message_listeners:
            try:
                message_listener.on_device_message(
                    message=DeviceMessage(
                        device_id=device_id,
                        timestamp=epochmillis_to_datetime(timestamp_millis, self._tz)
                        if timestamp_millis is not None else datetime.now(tz=self._tz),
                        payload=payload
                    ),
                )
            except Exception as e:
                logging.exception(e)
                raise
