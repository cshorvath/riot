import json
import unittest
from unittest.mock import Mock

import pytz

from data_processor.mqtt.data_observer import DataObserver, DeviceMessage
from data_processor.util import epochmillis_to_datetime

dummy_correct_message = {
    "timestamp": 1576482498000,
    "payload": {
        "a": 1,
        "b": 2
    }
}


class DataObserverUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data_observer = DataObserver()

    def tearDown(self) -> None:
        super().tearDown()

    def test_on_message_one_listener(self):
        mock_listener = Mock()
        self.data_observer.add_listener(mock_listener)
        self.data_observer.on_message(
            "riot/device/2/outgoing", json.dumps(dummy_correct_message))
        self.assertMessageTransform(dummy_correct_message, 2, self.get_on_device_message_arg(mock_listener))

    def test_on_message_multiple_listener(self):
        mock_listeners = [Mock(), Mock()]
        for listener in mock_listeners:
            self.data_observer.add_listener(listener)
        self.data_observer.on_message(
            "riot/device/2/outgoing", json.dumps(dummy_correct_message))
        for listener in mock_listeners:
            self.assertMessageTransform(dummy_correct_message, 2, self.get_on_device_message_arg(listener))

    def test_invalid_json_input(self):
        mock_listener = Mock()
        self.data_observer.add_listener(mock_listener)
        self.data_observer.on_message("riot/device/2/outgoing", "me not a json:)")
        mock_listener.on_device_message.assert_not_called()

    def test_invalid_device_id(self):
        mock_listener = Mock()
        self.data_observer.add_listener(mock_listener)
        self.data_observer.on_message("riot/device/menota/outgoing", json.dumps(dummy_correct_message))
        message = self.get_on_device_message_arg(mock_listener)
        self.assertMessageTransform(dummy_correct_message, -1, message)

    def get_on_device_message_arg(self, mock):
        return mock.on_device_message.call_args_list[0][1]['message']

    def assertMessageTransform(self, raw_message: dict, device_id: int, device_message: DeviceMessage):
        self.assertEqual(
            epochmillis_to_datetime(raw_message["timestamp"], pytz.utc),
            device_message.timestamp
        )
        self.assertDictEqual(
            device_message.payload, raw_message["payload"]
        )
        self.assertEqual(device_id, device_message.device_id)


if __name__ == '__main__':
    unittest.main()
