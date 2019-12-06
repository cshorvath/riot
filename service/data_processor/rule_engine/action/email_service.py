import asyncio
import logging
import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import List, Type

from core.model import Rule
from data_processor.mqtt.data_observer import DeviceMessage
from data_processor.rule_engine.action.action import ActionException, ActionHandler


class EmailService(ActionHandler, ABC):

    def run_action(self, message: DeviceMessage, rule: Rule, rule_message: str):
        self._send_mail(
            recipients=rule.action_arg.split(","),
            subject=f"'{rule.name}' triggered by device[name: {rule.source_device.name}"
                    f", id: {rule.source_device_id}]",
            body=f"Evaluated rule: {rule.name}\n"
                 f"{rule_message}\n\nTimestamp: {message.timestamp} \n"
                 f"Complete payload: {message.payload}"
        )

    @abstractmethod
    def _send_mail(self, recipients: List[str], subject: str, body: str):
        pass


class DummyEmailService(EmailService):

    def _send_mail(self, recipients: List[str], subject: str, body: str):
        logging.info(f"DUMMY mail sent: target[{recipients}], subject[{subject}], body[f{body}]")


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

    def _send_mail(self, recipients: List[str], subject: str, body: str):
        try:
            with self._smtp_class(
                    host=self._smtp_host,
                    port=self._smtp_port,
            ) as smtp_client:
                smtp_client.login(self._user, self._password)
                smtp_client.send_message(
                    msg=self._compose_msg(recipients, subject, body),
                    from_addr=self._from[1],
                    to_addrs=recipients
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


def email_service_factory(impl: str, config: dict) -> EmailService:
    if impl == "dummy":
        return DummyEmailService()
    if impl == "smtp":
        return SMTPEmailService(
            config["host"],
            config["port"],
            config["user"],
            config["password"],
            config["from_address"],
            config["from_name"],
            config["use_ssl"]
        )
