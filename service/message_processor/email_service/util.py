from message_processor.rule_engine.email_service import DummyEmailService, EmailService
from message_processor.rule_engine.email_service.smtp import SMTPEmailService


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
