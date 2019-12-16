from datetime import datetime

from data_processor.mqtt.data_observer import DeviceMessage

dummy_message = DeviceMessage(
    timestamp=datetime.now(),
    device_id=1,
    payload={
        "a": 1,
        "b": 2,
        "c": 3,
        "4": 3
    }
)
