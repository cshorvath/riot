import logging

from message_processor.data_observer import DataObserver
from message_processor.db.bootstrap import get_db_session
from message_processor.db.db_persister import DBPersister
from message_processor.rule_engine.email_service import DummyEmailService
from message_processor.rule_engine.rule_engine import RuleEngine

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.INFO)


def main():
    email_service = DummyEmailService()
    with get_db_session() as db_session:
        db_persister = DBPersister(db_session)
        rule_engine = RuleEngine(db_persister, email_service)
        data_observer = DataObserver(
            topics=["riot/device/#"],
            mqtt_broker_host="localhost"
        )
        data_observer.add_listener(db_persister)
        data_observer.add_listener(rule_engine)
        data_observer.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
