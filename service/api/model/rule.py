from typing import Optional

from pydantic.types import constr

from api.model.common import CommonModel
from api.model.device import Device
from api.model.user import User
from core.model import RuleOperator, ActionType


class RuleResponse(CommonModel):
    id: int
    name: constr(strip_whitespace=True, min_length=2, max_length=25)
    target_device: Optional[Device]
    creator: User
    message_field: str
    action_type: ActionType
    action_arg: str
    operator: RuleOperator
    operator_arg_1: float
    operator_arg_2: float


class NewRule(CommonModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=25)
    target_device_id: Optional[int]
    message_field: str
    action_type: ActionType
    action_arg: str
    operator: RuleOperator
    operator_arg_1: float
    operator_arg_2: float


class PatchRule(CommonModel):
    name: Optional[constr(strip_whitespace=True, min_length=2, max_length=25)]
    target_device_id: Optional[Optional[int]]
    message_field: Optional[str]
    action_type: Optional[ActionType]
    action_arg: Optional[str]
    operator: Optional[RuleOperator]
    operator_arg_1: Optional[float]
    operator_arg_2: Optional[float]
