import logging
from typing import List

from sqlalchemy import exists
from sqlalchemy.orm import Session

from core.model.model import Message, Device, Rule
from message_processor.mqtt.data_observer import DeviceMessageListener, DeviceMessage


class DBPersister(DeviceMessageListener):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def on_device_message(self, message: DeviceMessage):
        if not self._db_session.query(exists().where(Device.id == message.device_id)).scalar():
            logging.warning(f"Device[{message.device_id}] does not exists, will be created")
            self._db_session.add(DBPersister.create_dummy_device(message.device_id))
        message_dto = Message(
            device_id=message.device_id,
            timestamp=message.timestamp,
            direction=message.direction,
            payload=message.payload
        )
        self._db_session.add(message_dto)
        self._db_session.commit()

    @staticmethod
    def create_dummy_device(device_id):
        return Device(id=device_id, name=f"Unnamed {device_id}")

    def get_rules_for_device(self, device_id: int) -> List[Rule]:
        return self._db_session.query(Rule).filter_by(source_device_id=device_id).all()
