import json
from datetime import datetime

from sqlalchemy.orm import session

from common.model.model import Message, MessageDirection


class DBPersister:
    def __init__(self, db_session: session) -> None:
        self._db_session = db_session

    def store_message(self, device_id: int, direction: MessageDirection, timestamp: datetime, payload: dict):
        message = Message(
            device_id=device_id,
            timestamp=timestamp,
            direction=direction,
            payload=json.dumps(payload)
        )
        self._db_session.add(message)
        self._db_session.commit()
