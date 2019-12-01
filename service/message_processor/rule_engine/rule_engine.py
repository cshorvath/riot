import logging
from typing import Dict, List, Callable, Union, Optional, Tuple

from core.model.model import MessageDirection, RuleOperator, Rule, ActionType
from message_processor.db.db_persister import DBPersister
from message_processor.email_service import EmailService
from message_processor.mqtt.data_observer import DeviceMessageListener, DeviceMessage

Num = Union[int, float]


class RuleCondition:
    def __init__(self, message: str, predicate: Callable[[Num, Num, Num], bool]) -> None:
        self._message = message
        self._predicate = predicate

    def eval(self, x: Num, arg1: Num, arg2: Num) -> Tuple[bool, Optional[str]]:
        result = self._predicate(x, arg1, arg2)
        return result, self._message.format(x=x, arg1=arg1, arg2=arg2) if result else None


class RuleEngine(DeviceMessageListener):
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

    def __init__(self,
                 db_persister: DBPersister,
                 email_service: EmailService
                 ) -> None:
        self._email_service = email_service
        self.db_persister = db_persister

    def on_device_message(self, message: DeviceMessage):
        if message.direction != MessageDirection.INBOUND:
            return
        rules: List[Rule] = self.db_persister.get_rules_for_device(message.device_id)
        for rule in rules:
            try:
                condition = RuleEngine.operator_mapping[rule.operator]
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
                    if rule.action_type == ActionType.SEND_EMAIL:
                        self._email_service.send_mail(
                            recipients=rule.action_arg.split(","),
                            subject=f"'{rule.name}' triggered by device[name: {rule.source_device.name}"
                                    f", id: {rule.source_device_id}]",
                            body=f"Evaluated rule: {rule.name}\n"
                                 f"{rule_message}\n\nTimestamp: {message.timestamp} \n"
                                 f"Complete payload: {message.payload}"
                        )
                    elif rule.action_type == ActionType.FORWARD:
                        pass
            except KeyError:
                logging.error(f"Unable to find key {rule.message_field} in payload. Device[{message.device_id}],"
                              f" timestamp[{message.timestamp}] payload[{message.payload}]")
