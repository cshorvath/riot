import logging
import pprint

import pytz

from core.bootstrap import get_db_engine, get_db_session
from core.model.model import ActionType
from core.util import parse_config_from_env
from message_processor.db.db_persister import DBPersister
from message_processor.mqtt.data_observer import DataObserver
from message_processor.mqtt.mqtt_wrapper import MQTTClientWrapper
from message_processor.rule_engine.action.action import ActionHandler
from message_processor.rule_engine.action.email_service import email_service_factory
from message_processor.rule_engine.rule_engine import RuleEngine
from message_processor.rule_engine.util import get_input_topic_pattern

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.INFO)


def main():
    config = parse_config_from_env("RIOT_DATA_PROCESSOR_CONFIG")

    logging.info(f"Data processior is started, configuration:\n{pprint.pformat(config)}")

    email_service: ActionHandler = email_service_factory(
        config["email"]["implementation"],
        config["email"].get("arguments", None)
    )

    db_engine = get_db_engine(
        host=config["db"]["host"],
        port=config["db"]["port"],
        user=config["db"]["user"],
        password=config["db"]["password"],
        db=config["db"]["database"]
    )

    with get_db_session(db_engine) as db_session:
        mqtt_client = MQTTClientWrapper(
            client_id=config["mqtt"]["client_id"],
            mqtt_broker_host=config["mqtt"]["host"],
            mqtt_broker_port=config["mqtt"]["port"],
            topics=[get_input_topic_pattern(config["mqtt"]["topic_name_prefix"])],
            qos=1
        )
        db_persister = DBPersister(db_session)
        rule_engine = RuleEngine(db_persister)

        rule_engine.register_action_handler(ActionType.SEND_EMAIL, email_service)
        rule_engine.register_action_handler(ActionType.FORWARD, email_service)

        data_observer = DataObserver(tz=pytz.timezone(config["timezone"]))

        data_observer.add_listener(db_persister)
        data_observer.add_listener(rule_engine)

        mqtt_client.observer = data_observer
        mqtt_client.start()


if __name__ == "__main__":
    try:
        main()
    ex
    except AssertionError as e:
        logging.error("Assertion failed: " + str(e))
    except KeyboardInterrupt:
        pass
