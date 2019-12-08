from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from core.model import Message

MAX_MESSAGE_PER_PAGE = 100


def get_messages(db: Session, device_id: int, begin: datetime, end: datetime, page=0):
    filters = [Message.device_id == device_id]
    if begin:
        filters.append(Message.timestamp >= begin)
    if end:
        filters.append(Message.timestamp <= end)
    return db.query(Message).filter(and_(*filters)).limit(MAX_MESSAGE_PER_PAGE).offset(
        page * MAX_MESSAGE_PER_PAGE).all()
