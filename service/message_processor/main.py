import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import paho.mqtt.client as mqtt

# todo config
from message_processor.db.db_persister import DBPersister
from message_processor.mqtt_client import DataObserver


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine('mysql+mysqldb://riot:riot@127.0.0.1/riot', convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine))

mqtt_client = mqtt.Client("riot_data_processor", clean_session=False)
db_persister = DBPersister(db_session)
data_observer = DataObserver(mqtt_client, db_persister)
data_observer.start("riot/device/#", "localhost")

while True:
    data_observer.step()
