import json
import unittest
from unittest.mock import Mock

from core.model import Rule
from data_processor.rule_engine.action.message_forwarder import MessageForwarder
from data_processor.testing.util import dummy_message
from data_processor.util import get_output_topic


class MessageForwarderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.mqtt_wrapper = Mock()
        self.db_persister = Mock()
        self.message_forwarder = MessageForwarder(self.mqtt_wrapper, self.db_persister, "riot")

        def publish_json_mock(topic, payload, cb):
            cb()

        self.mqtt_wrapper.publish_json.side_effect = publish_json_mock

        self.message_format_with_original_message = {
            "foo": 1,
            "bar": 2,
            "original_message": None
        }

        self.message_format_without_original_message = {
            "foo": 1,
            "bar": 2
        }

    def test_original_message_included(self):
        self.message_forwarder.run_action(dummy_message, Rule(target_device_id=2, action_arg=json.dumps(
            self.message_format_with_original_message)), "")
        self.message_format_with_original_message["original_message"] = dummy_message.to_json()
        self.assert_publish_json_call(get_output_topic("riot", 2), self.message_format_with_original_message)
        self.db_persister.store_message.assert_called_once()

    def test_original_message_excluded(self):
        self.message_forwarder.run_action(dummy_message, Rule(target_device_id=2, action_arg=json.dumps(
            self.message_format_without_original_message)), "")
        self.assert_publish_json_call(get_output_topic("riot", 2), self.message_format_without_original_message)
        self.db_persister.store_message.assert_called_once()

    def test_non_json_message_format(self):
        self.message_forwarder.run_action(dummy_message, Rule(target_device_id=2, action_arg=json.dumps("me not json")),
                                          "")
        self.assert_publish_json_call(get_output_topic("riot", 2), "me not json")
        self.db_persister.store_message.assert_called_once()

    def assert_publish_json_call(self, topic, message):
        self.mqtt_wrapper.publish_json.assert_called_once()
        self.assertEqual(self.mqtt_wrapper.publish_json.call_args_list[0][1]['topic'], topic)
        published = self.mqtt_wrapper.publish_json.call_args_list[0][1]['payload']

        self.assertEqual(published["payload"], message)


if __name__ == '__main__':
    unittest.main()
