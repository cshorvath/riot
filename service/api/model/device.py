from api.model.common import CommonModel


class Device(CommonModel):
    name: str
    description: str


class DeviceResponse(Device):
    id: int
