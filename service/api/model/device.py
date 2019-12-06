from typing import List

from api.model.common import CommonModel
from api.model.user import User


class Device(CommonModel):
    name: str
    description: str


class DeviceResponse(Device):
    id: id
    owners: List[User]
