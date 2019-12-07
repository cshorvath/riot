from api.model.common import CommonModel


class User(CommonModel):
    id: int
    name: str
    admin: bool


class NewUser(CommonModel):
    name: str
    password: str
