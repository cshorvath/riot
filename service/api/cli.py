import logging
import sys
from getpass import getpass

from api.bootstrap import db_engine
from api.repository.user import create_user
from core.bootstrap import get_db_session
from core.model import User


def create_user_cli():
    username, password = "", ""
    while not (username.strip(" ") and len(username.strip(" ")) >= 3):
        username = input("Username: ")
    while not password:
        password = getpass("Password: ")
    admin_str = input("Admin [no, type yes to make admin]: ")
    admin = admin_str.lower() == "yes"

    with get_db_session(db_engine) as db_session:
        exists = db_session.query(User.name).filter_by(name=username).scalar() is not None
        if exists:
            logging.error(f"User with name {username} already exists")
            sys.exit(1)
        create_user(db_session, username, password, admin)

    logging.info(f"User [{username}, admin: {admin}] created.")
