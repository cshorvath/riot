import json
import logging
from datetime import datetime
from typing import Callable

from core.model import Rule, MessageDirection
from data_processor.db.db_persister import DBPersister
from data_processor.mqtt.data_observer import DeviceMessage
from data_processor.mqtt.mqtt_wrapper import MQTTClientWrapper
from data_processor.rule_engine.action.action import ActionHandler
from data_processor.util import datetime_to_epochmillis, get_output_topic


class MessageForwarder(ActionHandler):

    def __init__(self, mqtt_wrapper: MQTTClientWrapper, db_persister: DBPersister, prefix: str) -> None:
        self._prefix = prefix
        self._mqtt_wrapper = mqtt_wrapper
        self._db_persister = db_persister

    def run_action(self, message: DeviceMessage, rule: Rule, rule_message: str):
        topic_name = get_output_topic(self._prefix, rule.target_device_id)
        try:
            out_payload = json.loads(rule.action_arg)
            if "original_message" in out_payload:
                out_payload["original_message"] = message.to_json()
        except json.JSONDecodeError:
            logging.debug(f"{rule.action_arg} is not a valid json")
            out_payload = rule.action_arg
        timestamp = datetime.now()
        out_message = {
            "timestamp": datetime_to_epochmillis(timestamp),
            "payload": out_payload
        }
        self._mqtt_wrapper.publish_json(
            topic=topic_name,
            payload=out_message,
            cb=self._get_on_publish_callback(rule.target_device_id, timestamp, out_payload)
        )

    def _get_on_publish_callback(self, device_id: int, timestamp: datetime, out_payload: dict) -> Callable[[], None]:
        return lambda: self._db_persister.store_message(
            message=DeviceMessage(device_id, timestamp, out_payload),
            direction=MessageDirection.OUTBOUND
        )
