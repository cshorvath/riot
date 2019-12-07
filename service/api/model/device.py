from typing import List

from pydantic.types import constr

from api.model.common import CommonModel
from api.model.user import User


class Device(CommonModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=25)
    description: str


class DeviceResponse(Device):
    id: int
    owners: List[User]
