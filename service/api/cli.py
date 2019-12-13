import logging
from getpass import getpass

from api.bootstrap import db_engine
from api.repository.user import create_user
from core.bootstrap import get_db_session


def create_user_cli():
    username, password = "", ""
    while not username.strip(" "):
        username = input("Admin username: ")
    while not password:
        password = getpass("Admin password: ")
    admin_str = input("Admin [no, type yes to make admin]: ")
    admin = admin_str.lower() == "yes"

    with get_db_session(db_engine) as db_session:
        create_user(db_session, username, password, admin)

    logging.info(f"Admin user [{username}] created.")
