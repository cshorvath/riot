from typing import Union

from pydantic.networks import EmailStr
from pydantic.types import constr

from api.model.common import CommonModel
from api.model.device import Device
from api.model.user import User
from core.model import RuleOperator, ActionType


class EmailAction(CommonModel):
    target_address: EmailStr


class ForwardAction(CommonModel):
    target_device: Device
    message: dict


class RuleResponse(CommonModel):
    id: int
    name: constr(strip_whitespace=True, min_length=2, max_length=25)
    target_device: Device
    creator: User
    message_field: str
    action_type: ActionType
    action_arg1: str
    action_arg2: str
    operator: RuleOperator
    operator_arg1: Union[int, float]
    operator_arg2: Union[int, float]


class NewRule(CommonModel):
    id: int
    name: constr(strip_whitespace=True, min_length=2, max_length=25)
    target_device_id: int
    message_field: str
    action_type: ActionType
    action_arg1: str
    action_arg2: str
    operator: RuleOperator
    operator_arg1: Union[int, float]
    operator_arg2: Union[int, float]
