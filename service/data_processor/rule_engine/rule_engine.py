import logging
from numbers import Number
from typing import List, Dict, Callable, Tuple, Optional

from core.model import RuleOperator, ActionType, Rule
from data_processor.db.db_persister import DBPersister
from data_processor.mqtt.data_observer import DeviceMessageListener, DeviceMessage
from data_processor.rule_engine.action.action import ActionHandler, ActionException


class RuleCondition:
    def __init__(self, message: str, predicate: Callable[[Number, Number, Number], bool]) -> None:
        self._message = message
        self._predicate = predicate

    def eval(self, x: Number, arg1: Number, arg2: Number) -> Tuple[bool, Optional[str]]:
        result = self._predicate(x, arg1, arg2)
        return result, self._message.format(x=x, arg1=arg1, arg2=arg2) if result else None


operator_mapping: Dict[RuleOperator, RuleCondition] = {
    RuleOperator.LT:
        RuleCondition("{x} < {arg1}", lambda x, arg1, arg2: x < arg1),
    RuleOperator.LTE:
        RuleCondition("{x} <= {arg1}", lambda x, arg1, arg2: x <= arg1),
    RuleOperator.GT:
        RuleCondition("{x} > {arg1}", lambda x, arg1, arg2: x > arg1),
    RuleOperator.GTE:
        RuleCondition("{x} >= {arg1}", lambda x, arg1, arg2: x >= arg1),
    RuleOperator.EQ:
        RuleCondition("{x} == {arg1}", lambda x, arg1, arg2: x == arg1),
    RuleOperator.NE:
        RuleCondition("{x} != {arg1}", lambda x, arg1, arg2: x != arg1),
    RuleOperator.BETWEEN:
        RuleCondition("{arg1} <= {x} <= {arg2}", lambda x, arg1, arg2: x <= arg1 and x <= arg2),
    RuleOperator.ANY:
        RuleCondition("Value present {x}", lambda x, arg1, arg2: True)
}


class RuleEngine(DeviceMessageListener):

    def __init__(self, db_persister: DBPersister) -> None:
        self._db_persister = db_persister
        self._action_handlers: Dict[ActionType, ActionHandler] = {}

    def register_action_handler(self, action_type: ActionType, handler: ActionHandler):
        self._action_handlers[action_type] = handler

    def on_device_message(self, message: DeviceMessage):
        rules: List[Rule] = self._db_persister.get_rules_for_device(message.device_id)
        for rule in rules:
            try:
                condition = operator_mapping[rule.operator]
            except KeyError:
                logging.error(f"Unable to evaluate operator in Rule[{rule}]")
                continue
            try:
                result, rule_message = condition.eval(
                    x=message.payload[rule.message_field],
                    arg1=rule.operator_arg_1,
                    arg2=rule.operator_arg_2
                )
                if result:
                    action_handler = self._action_handlers.get(rule.action_type, None)
                    if not action_handler:
                        logging.error(f"Missing action handler for type {rule.action_type}, rule[{rule.id}]")
                        continue
                    action_handler.run_action(message, rule, rule_message)
            except KeyError:
                logging.error(f"Unable to find key {rule.message_field} in payload. Device[{message.device_id}],"
                              f" timestamp[{message.timestamp}] payload[{message.payload}]")
            except ActionException as ex:
                logging.exception(ex)
