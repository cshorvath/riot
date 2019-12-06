from numbers import Number
from typing import Union

from pydantic.networks import EmailStr

from api.model.common import CommonModel
from api.model.device import Device
from api.model.user import User
from core.model import RuleOperator


class EmailAction(CommonModel):
    target_address: EmailStr


class ForwardAction(CommonModel):
    target_device_id: int
    message: dict


class Rule(CommonModel):
    source_device: Device
    target_device: Device
    creator: User
    message_field: str
    action: Union[EmailAction, ForwardAction]
    operator: RuleOperator
    operator_arg1: Number
    operator_arg2: Number


class RuleResponse(Rule):
    id: int
