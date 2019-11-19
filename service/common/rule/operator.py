from abc import ABC, abstractmethod

from common.model.model import RuleOperatorId


class RuleOperator(ABC):

    def __init__(self, model_id: RuleOperatorId, arg_count: int) -> None:
        self.model_id = model_id
        self.arg_count = arg_count

    def check_arg_count(self, args):
        assert len(args) == self.arg_count

    def eval(self, *args):
        self.check_arg_count(args)

    @abstractmethod
    def _eval(self):
        pass


class LessThan(RuleOperator):

    def __init__(self) -> None:
        super().__init__(RuleOperatorId.LT, 1)

    def _eval(self, *args):
        pass
