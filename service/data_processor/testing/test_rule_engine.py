import unittest
from typing import List
from unittest.mock import Mock

from core.model import Rule, RuleOperator, ActionType
from data_processor.rule_engine.rule_engine import RuleEngine
from data_processor.testing.util import dummy_message


class RuleEngineUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        self._db_persister = Mock()
        self.rule_engine = RuleEngine(self._db_persister)
        self.email_handler = Mock()
        self.forward_handler = Mock()
        self.rule_engine.register_action_handler(ActionType.SEND_EMAIL, self.email_handler)
        self.rule_engine.register_action_handler(ActionType.FORWARD, self.forward_handler)

    def test_rules_must_be_triggeded(self):
        for action_type in (ActionType.FORWARD, ActionType.SEND_EMAIL):
            with self.subTest(action_type=action_type):
                rules = [
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.LT, operator_arg_1=2, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.LTE, operator_arg_1=1, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.GT, operator_arg_1=0, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.GTE, operator_arg_1=1, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.EQ, operator_arg_1=1, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.NE, operator_arg_1=34, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.BETWEEN, operator_arg_1=-1, operator_arg_2=3,
                         action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.ANY, action_type=action_type)
                ]
                self.set_rules_to_return(rules)
                handler = self.email_handler if action_type == ActionType.SEND_EMAIL else self.forward_handler
                self.rule_engine.on_device_message(dummy_message)
                self.assertEqual(handler.run_action.call_count, 8)

    def test_rules_must_not_be_triggeded(self):
        for action_type in (ActionType.FORWARD, ActionType.SEND_EMAIL):
            with self.subTest(action_type=action_type):
                rules = [
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.LT, operator_arg_1=1, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.LTE, operator_arg_1=0, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.GT, operator_arg_1=1, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.GTE, operator_arg_1=3, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.EQ, operator_arg_1=0, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.NE, operator_arg_1=1, action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="a", operator=RuleOperator.BETWEEN, operator_arg_1=3, operator_arg_2=8,
                         action_type=action_type),
                    Rule(source_device_id=1, name="1",
                         message_field="d", operator=RuleOperator.ANY, action_type=action_type)
                ]
                self.set_rules_to_return(rules)
                handler = self.email_handler if action_type == ActionType.SEND_EMAIL else self.forward_handler
                self.rule_engine.on_device_message(dummy_message)
                handler.run_action.assert_not_called()

    def set_rules_to_return(self, rules: List[Rule]):
        self._db_persister.get_rules_for_device = lambda x: rules


if __name__ == '__main__':
    unittest.main()
