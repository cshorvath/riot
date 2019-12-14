import logging
import sys

import pytz

from core.bootstrap import get_db_engine, get_db_session, migrate
from core.model import ActionType
from core.util import parse_config_from_env, MissingConfigKeyException, ConfigNode
from data_processor.db.db_persister import DBPersister
from data_processor.mqtt.data_observer import DataObserver
from data_processor.mqtt.mqtt_wrapper import MQTTClientWrapper
from data_processor.rule_engine.action.action import ActionHandler
from data_processor.rule_engine.action.email_service import email_service_factory
from data_processor.rule_engine.action.message_forwarder import MessageForwarder
from data_processor.rule_engine.rule_engine import RuleEngine
from data_processor.util import get_input_topic_pattern

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.DEBUG)


def main():
    config: ConfigNode = parse_config_from_env("RIOT_DATA_PROCESSOR_CONFIG")
    logging.info(f"Data processor is started, configuration:\n{config}")

    db_engine = get_db_engine(
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
        db=config.db.database
    )

    migrate(db_engine)

    email_service: ActionHandler = email_service_factory(
        config.email.implementation,
        config.email.get_optional("arguments")
    )

    with get_db_session(db_engine) as db_session:
        topic_prefix = config.mqtt.topic_name_prefix
        qos = config.mqtt.qos
        timezone = pytz.timezone(config.timezone)

        mqtt_client = MQTTClientWrapper(
            client_id=config.mqtt.client_id,
            mqtt_broker_host=config.mqtt.host,
            mqtt_broker_port=config.mqtt.port,
            topics=[get_input_topic_pattern(topic_prefix)],
            qos=qos
        )
        db_persister = DBPersister(db_session)

        message_forwarder: ActionHandler = MessageForwarder(
            mqtt_wrapper=mqtt_client,
            db_persister=db_persister,
            prefix=topic_prefix,
            qos=qos,
            tz=timezone
        )

        rule_engine = RuleEngine(db_persister)
        rule_engine.register_action_handler(ActionType.SEND_EMAIL, email_service)
        rule_engine.register_action_handler(ActionType.FORWARD, message_forwarder)

        data_observer = DataObserver(tz=timezone)

        data_observer.add_listener(db_persister)
        data_observer.add_listener(rule_engine)

        mqtt_client.add_subscriber(data_observer)
        mqtt_client.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except MissingConfigKeyException as e:
        logging.error(e.message)
    except AssertionError as e:
        logging.error("Assertion failed: " + str(e))
    except Exception as e:
        logging.exception(e)
    sys.exit(1)
