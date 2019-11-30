import logging
from abc import ABC, abstractmethod
from typing import List


class EmailService(ABC):
    @abstractmethod
    def send_mail(self, recipients: List[str], subject: str, body: str):
        pass


class DummyEmailService(EmailService):

    def send_mail(self, recipients: List[str], subject: str, body: str):
        logging.info(f"DUMMY mail sent: target[{recipients}], subject[{subject}], body[f{body}]")
