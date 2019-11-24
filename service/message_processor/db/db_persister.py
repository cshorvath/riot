import json
from datetime import datetime

from sqlalchemy.orm import session

from common.model.model import Message, MessageDirection
from message_processor.util import MessageListener


class DBPersister(MessageListener):
    def __init__(self, db_session: session) -> None:
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

    def store_message(self, device_id: int, direction: MessageDirection, timestamp: int, payload: dict):
        message = Message(
            device_id=device_id,
            timestamp=datetime.fromtimestamp(timestamp / 1000),
            direction=direction,
            payload=json.dumps(payload)
        )
        self._db_session.add(message)
        self._db_session.commit()
