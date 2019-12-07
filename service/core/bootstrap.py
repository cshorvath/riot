import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_db_engine(host, user, password, db, port=3306):
    return create_engine(f"mysql+mysqldb://{user}:{password}@{host}:{port}/{db}", convert_unicode=True)


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
        logging.info("Database session closed")
