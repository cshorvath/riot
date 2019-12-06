from api.model.common import CommonModel


class User(CommonModel):
    id: int
    name: str
    is_admin: bool


class NewUser(CommonModel):
    name: str
    password: str
