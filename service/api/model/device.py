from typing import Optional

from pydantic.types import constr

from api.model.common import CommonModel


class Device(CommonModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=25)
    description: Optional[str]


class DeviceResponse(Device):
    id: int
    rule_count: Optional[int]
