import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.model import Base


def get_db_engine(host, user, password, db, port=3306):
    return create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}?charset=utf8",
                         convert_unicode=True)


def migrate(engine):
    Base.metadata.create_all(engine)


@contextmanager
def get_db_session(engine):
    Session = sessionmaker(autocommit=False,
                           autoflush=False,
                           bind=engine)
    try:
        session = Session()
        yield session
    finally:
        session.close()
        logging.debug("Database session closed")
