class NotFoundException(Exception):
    def __init__(self, key) -> None:
        self.key = key
        self.message = f"{key} not found"
