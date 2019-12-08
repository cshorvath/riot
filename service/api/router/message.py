from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.repository.message as message_repository
from api.bootstrap import get_db
from api.model.message import Message
from api.util.auth import owner_user

router = APIRouter()


@router.get("/{device_id}/message", dependencies=[Depends(owner_user)], response_model=List[Message])
def get_messages(
        device_id: int,
        begin: datetime = None,
        end: datetime = None,
        page: int = 0,
        db: Session = Depends(get_db)):
    return message_repository.get_messages(db, device_id, begin, end, page)
