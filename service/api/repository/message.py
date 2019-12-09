from datetime import datetime
from typing import Tuple, List

from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from core.model import Message

MAX_MESSAGE_PER_PAGE = 100


def get_messages(db: Session, device_id: int, begin: datetime, end: datetime, page=1) -> Tuple[List[Message], int]:
    filters = [Message.device_id == device_id]
    if begin:
        filters.append(Message.timestamp >= begin)
    if end:
        filters.append(Message.timestamp <= end)

    query: Query = db.query(Message).filter(and_(*filters))
    record_count = query.count()
    return query.limit(MAX_MESSAGE_PER_PAGE).offset((page - 1) * MAX_MESSAGE_PER_PAGE).all(), record_count
