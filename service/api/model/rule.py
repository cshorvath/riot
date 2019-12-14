from typing import Optional

from pydantic.types import constr

from api.model.common import CommonModel
from api.model.device import DeviceResponse
from api.model.user import User
from core.model import RuleOperator, ActionType


class RuleResponse(CommonModel):
    id: int
    name: constr(strip_whitespace=True, min_length=2, max_length=100)
    target_device: Optional[DeviceResponse]
    creator: User
    message_field: str
    action_type: ActionType
    action_arg: str
    operator: RuleOperator
    operator_arg_1: Optional[float]
    operator_arg_2: Optional[float]


class RuleRequest(CommonModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=100)
    target_device_id: Optional[int]
    message_field: str
    action_type: ActionType
    action_arg: str
    operator: RuleOperator
    operator_arg_1: Optional[float]
    operator_arg_2: Optional[float]
