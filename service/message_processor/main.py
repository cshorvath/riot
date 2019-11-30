import logging

from core.util import parse_config_from_env
from message_processor.data_observer import DataObserver
from message_processor.db.bootstrap import get_db_session, get_db_engine
from message_processor.db.db_persister import DBPersister
from message_processor.email_service import EmailService
from message_processor.email_service.util import email_service_factory
from message_processor.rule_engine.rule_engine import RuleEngine

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.INFO)


def main():
    config = parse_config_from_env("RIOT_DATA_PROCESSOR_CONFIG")

    email_service: EmailService = email_service_factory(
        config["email"]["implementation"],
        config["email"]["arguments"]
    )

    db_engine = get_db_engine(
        config["db"]["host"],
        config["db"]["user"],
        config["db"]["password"],
        config["db"]["database"],
        config["db"]["port"]
    )

    with get_db_session(db_engine) as db_session:
        db_persister = DBPersister(db_session)
        rule_engine = RuleEngine(db_persister, email_service)
        data_observer = DataObserver(
            topics=["riot/device/#"],
            mqtt_broker_host=config["mqtt"]["host"],
            mqtt_broker_port=config["mqtt"]["port"]
        )
        data_observer.add_listener(db_persister)
        data_observer.add_listener(rule_engine)
        data_observer.start()


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        logging.error("Assertion failed: " + str(e))
    except KeyboardInterrupt:
        pass
