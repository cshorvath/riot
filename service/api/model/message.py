from datetime import datetime

from api.model.common import CommonModel
from core.model import MessageDirection


class Message(CommonModel):
    id: int
    device_id: int
    timestamp: datetime
    payload: dict
    direction: MessageDirection


class OutgoingMessage(CommonModel):
    device_id: int
    payload: dict
