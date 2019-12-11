import logging

from api.bootstrap import config, db_engine
from api.repository.user import create_user
from core.bootstrap import get_db_session
from core.model import Base

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    logging.info(f"Migration started:\n{config.db}")

    logging.info("Drop all tables")
    Base.metadata.drop_all(bind=db_engine)
    logging.info("Create tables")
    Base.metadata.create_all(bind=db_engine)

    username, password = "", ""
    while not username.strip(" "):
        username = input("Admin username: ")
    while not password:
        password = input("Admin password: ")

    with get_db_session(db_engine) as db_session:
        create_user(db_session, username, password, True)

    logging.info(f"Admin user [{username}] created.")
