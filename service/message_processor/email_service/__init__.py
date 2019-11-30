import logging
from abc import ABC, abstractmethod
from typing import List, Tuple


class EmailService(ABC):
    @abstractmethod
    def send_mail(self, targets: List[Tuple[str, str]], subject: str, body: str):
        pass


class DummyEmailService(EmailService):

    def send_mail(self, targets: List[str], subject: str, body: str):
        logging.info(f"DUMMY mail sent: target[{targets}], subject[{subject}], body[f{body}]")
