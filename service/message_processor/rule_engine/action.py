class ActionException(Exception):
    def __init__(self, cause) -> None:
        super(ActionException, self).__init__("Action execution error" + repr(cause))
        self.cause = cause
