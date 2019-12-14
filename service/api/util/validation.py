from fastapi import HTTPException

from api.model.rule import RuleRequest
from core.model import ActionType, RuleOperator


def validate_rule(rule: RuleRequest):
    exception = HTTPException(status_code=422, detail="Invalid rule")
    if rule.action_type == ActionType.FORWARD and rule.target_device_id is None:
        raise exception
    if rule.operator != RuleOperator.ANY and rule.operator_arg_1 is None:
        raise exception
    if rule.operator == RuleOperator.BETWEEN and rule.operator_arg_2 is None:
        raise exception
