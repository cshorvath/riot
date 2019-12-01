from core.model.model import Rule
from message_processor.mqtt.data_observer import DeviceMessage
from message_processor.rule_engine.action.action import ActionHandler


class MessageForwarder(ActionHandler):
    def run_action(self, message: DeviceMessage, rule: Rule, rule_message: str):
        pass
