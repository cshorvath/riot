from core.model import MessageDirection
from data_processor.db.db_persister import DBPersister
from data_processor.mqtt.data_observer import DeviceMessageListener, DeviceMessage


class MessageInsertListener(DeviceMessageListener):
    def __init__(self, db_persister: DBPersister) -> None:
        self._db_persister = db_persister

    def on_device_message(self, message: DeviceMessage):
        self._db_persister.store_message(message, MessageDirection.INBOUND)
