import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

engine: Engine = create_engine('mysql+mysqldb://riot:riot@127.0.0.1/riot', convert_unicode=True)


@contextmanager
def get_db_session():
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
