import math

from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import conint
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

import api.repository.device as device_repository
import api.repository.message as message_repository
from api.bootstrap import get_db
from api.model.message import Message, MessageResponse
from api.util.auth import owner_user

router = APIRouter()


@router.get("/{device_id}/message", dependencies=[Depends(owner_user)], response_model=MessageResponse)
def get_messages(
        device_id: int,
        page: conint(ge=1) = 1,
        records_per_page: conint(ge=0) = 50,
        db: Session = Depends(get_db)):
    if not device_repository.get_device(db, device_id)[0]:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    messages, record_count = message_repository.get_messages(db, device_id, page, records_per_page)
    page_count = math.ceil(record_count / records_per_page)
    return MessageResponse(
        page=page,
        page_count=page_count,
        record_count=record_count,
        items=[Message.from_orm(msg) for msg in messages])
