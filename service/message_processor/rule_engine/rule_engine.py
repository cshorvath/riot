import logging
from typing import Dict, List, Callable, Union

from common.model.model import MessageDirection, RuleOperator, Rule
from message_processor.db.db_persister import DBPersister
from message_processor.rule_engine.email_service import EmailService
from message_processor.util import MessageListener


class RuleUpdateObserver(MessageListener):
    def on_message(self, device_id: int, timestamp: int, payload: dict,
                   direction: MessageDirection = MessageDirection.INBOUND):
        pass


Num = Union[int, float]


class RuleEvaluationError(BaseException):
    pass


class RuleEngine(MessageListener):
    operator_mapping: Dict[RuleOperator, Callable[[Num, Num, Num], bool]] = {
        RuleOperator.LT: lambda x, arg1, arg2: x < arg1,
        RuleOperator.LTE: lambda x, arg1, arg2: x <= arg1,
        RuleOperator.GT: lambda x, arg1, arg2: x > arg1,
        RuleOperator.GTE: lambda x, arg1, arg2: x >= arg1,
        RuleOperator.EQ: lambda x, arg1, arg2: x == arg1,
        RuleOperator.NE: lambda x, arg1, arg2: x != arg1,
        RuleOperator.BETWEEN: lambda x, arg1, arg2: x <= arg1 and x <= arg2,
        RuleOperator.ANY: lambda x, arg1, arg2: True
    }

    def __init__(self, db_persister: DBPersister, email_service: EmailService) -> None:
        self._email_service = email_service
        self.db_persister = db_persister

    def on_message(self,
                   device_id: int,
                   timestamp: int,
                   payload: dict,
                   direction: MessageDirection = MessageDirection.INBOUND):
        # TODO cache the rules
        if direction != MessageDirection.INBOUND:
            return
        rules: List[Rule] = self.db_persister.get_rules_for_device(device_id)
        for rule in rules:
            try:
                condition = RuleEngine.operator_mapping[rule.operator]
            except KeyError:
                logging.error(f"Unable to evaluate operator in Rule[{rule}]")
                continue
            try:
                if condition(payload[rule.message_field], rule.operator_arg_1, rule.operator_arg_2):
                    logging.info("sstart to send mail")
                    self._email_service.send_mail([("fo", rule.action_arg)], f"Device {device_id} sent msg",
                                                  str(payload))
                    logging.info("sent")
            except KeyError:
                logging.error(f"Unable to find key {rule.message_field} in payload. Device[{device_id}],"
                              f" timestamp[{timestamp}] payload[{payload}]")
