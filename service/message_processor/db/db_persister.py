import logging
from datetime import datetime

from sqlalchemy import exists
from sqlalchemy.orm import Session

from common.model.model import Message, MessageDirection, Device
from message_processor.util import MessageListener


class DBPersister(MessageListener):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def on_message(self,
                   device_id: int,
                   timestamp: int,
                   payload: dict,
                   direction: MessageDirection = MessageDirection.INBOUND):
        self.store_message(
            device_id,
            direction,
            timestamp,
            payload
        )

    @staticmethod
    def create_dummy_device(device_id):
        return Device(id=device_id, name=f"Unnamed {device_id}")

    def store_message(self, device_id: int, direction: MessageDirection, timestamp: int, payload: dict):
        if not self._db_session.query(exists().where(Device.id == device_id)).scalar():
            logging.warning(f"Device[{device_id}] does not exists, will be created")
            self._db_session.add(DBPersister.create_dummy_device(device_id))
        message = Message(
            device_id=device_id,
            timestamp=datetime.fromtimestamp(timestamp / 1000),
            direction=direction,
            payload=payload
        )
        self._db_session.add(message)
        self._db_session.commit()
