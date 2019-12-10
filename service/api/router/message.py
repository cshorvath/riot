import math
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic.types import conint
from sqlalchemy.orm import Session

import api.repository.message as message_repository
from api.bootstrap import get_db
from api.model.message import Message, MessageResponse
from api.util.auth import owner_user

router = APIRouter()


@router.get("/{device_id}/message", dependencies=[Depends(owner_user)], response_model=MessageResponse)
def get_messages(
        device_id: int,
        begin: datetime = None,
        end: datetime = None,
        page: conint(ge=1) = 1,
        records_per_page: conint(ge=0) = 100,
        db: Session = Depends(get_db)):
    messages, record_count = message_repository.get_messages(db, device_id, begin, end, page, records_per_page)
    page_count = math.ceil(record_count / records_per_page)
    return MessageResponse(
        page=page,
        page_count=page_count,
        record_count=record_count,
        items=[Message.from_orm(msg) for msg in messages])
