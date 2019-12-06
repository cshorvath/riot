import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session

from core.model import Base

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# todo parameters

engine: Engine = create_engine('mysql+mysqldb://riot:riot@127.0.0.1/riot', convert_unicode=True)
db_session: scoped_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine)
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
