from pydantic.main import BaseModel


class CommonModel(BaseModel):
    class Config:
        orm_mode = True
