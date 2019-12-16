from pydantic.types import constr

from api.model.common import CommonModel


class User(CommonModel):
    id: int
    name: constr(strip_whitespace=True, min_length=2, max_length=25)
    admin: bool
