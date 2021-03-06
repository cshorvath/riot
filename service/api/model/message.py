from datetime import datetime
from typing import List

from api.model.common import CommonModel


class Message(CommonModel):
    id: int
    device_id: int
    timestamp: datetime
    payload: dict


class MessageResponse(CommonModel):
    items: List[Message]
    page: int
    page_count: int
    record_count: int
