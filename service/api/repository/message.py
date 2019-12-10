from datetime import datetime
from typing import Tuple, List

from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from core.model import Message


def get_messages(db: Session, device_id: int, begin: datetime, end: datetime, page=1, records_per_page: int = 100) -> \
Tuple[List[Message], int]:
    filters = [Message.device_id == device_id]
    if begin:
        filters.append(Message.timestamp >= begin)
    if end:
        filters.append(Message.timestamp <= end)

    query: Query = db.query(Message).filter(and_(*filters))
    record_count = query.count()
    return query.limit(records_per_page).offset((page - 1) * records_per_page).all(), record_count
