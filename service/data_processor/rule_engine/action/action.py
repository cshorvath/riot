from abc import ABC, abstractmethod

from core.model import Rule
from data_processor.mqtt.data_observer import DeviceMessage


class ActionException(Exception):
    def __init__(self, cause) -> None:
        super(ActionException, self).__init__("Action execution error" + repr(cause))
        self.cause = cause


class ActionHandler(ABC):
    @abstractmethod
    def run_action(self, message: DeviceMessage, rule: Rule, rule_message: str):
        pass
