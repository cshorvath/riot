import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_engine(host, user, password, db, port=3306):
    return create_engine(f"mysql+mysqldb://{user}:{password}@{host}:{port}/{db}", convert_unicode=True)


@contextmanager
def get_db_session(engine):
    session = sessionmaker(autocommit=False,
                           autoflush=False,
                           bind=engine)()
    try:
        yield session
    except Exception as e:
        logging.error(f"Database error: {e}")
        session.rollback()
        raise
    finally:
        session.close()
        logging.info("Database session closed")
