from typing import Tuple, List

from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from core.model import Message, MessageDirection


def get_messages(db: Session, device_id: int, page=1, records_per_page: int = 50) -> Tuple[List[Message], int]:
    filters = [Message.device_id == device_id, Message.direction == MessageDirection.INBOUND]
    query: Query = db.query(Message).filter(and_(*filters))
    record_count = query.count()
    return query.limit(records_per_page).offset((page - 1) * records_per_page).all(), record_count
