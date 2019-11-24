import logging

from message_processor.data_observer import DataObserver
from message_processor.db.bootstrap import get_db_session
from message_processor.db.db_persister import DBPersister

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.INFO)


def main():
    with get_db_session() as db_session:
        db_persister = DBPersister(db_session)
        data_observer = DataObserver(
            topics=["riot/device/#"],
            mqtt_broker_host="localhost"
        )
        data_observer.add_listener(db_persister)
        data_observer.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
