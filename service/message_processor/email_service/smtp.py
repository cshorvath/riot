import asyncio
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import List, Type, Tuple

from message_processor.email_service import EmailService
from message_processor.rule_engine.action import ActionException


class SMTPEmailService(EmailService):

    def __init__(self,
                 smtp_host: str,
                 smtp_port: int,
                 user: str,
                 password: str,
                 from_address: str,
                 from_name: str = None,
                 use_ssl: bool = True):
        self._smtp_port = smtp_port
        self._smtp_host = smtp_host
        self._user = user
        self._password = password
        self._from = from_name, from_address
        self._smtp_class: Type[smtplib.SMTP] = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP_SSL
        self._mail_queue = asyncio.Queue()

    def send_mail(self, recipients: List[str], subject: str, body: str):
        try:
            with self._smtp_class(
                    host=self._smtp_host,
                    port=self._smtp_port,
            ) as smtp_client:
                smtp_client.login(self._user, self._password)
                smtp_client.send_message(
                    msg=self._compose_msg(recipients, subject, body)
                )
            logging.info(f"Message sent to [{recipients}], subject: {subject}")
        except smtplib.SMTPException as ex:
            raise ActionException(ex)

    def _compose_msg(self, recipients: List[str], subject: str, body: str):
        msg = MIMEText(body)
        msg["From"] = formataddr(self._from)
        msg["To"] = ",".join(recipients)
        msg["Subject"] = subject
        return msg
