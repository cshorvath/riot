from typing import Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import core.model as db_model
from api.util.auth import get_password_hash
from api.util.exception import NotFoundException


def get_user(db: Session, user_id: int) -> db_model.User:
    return db.query(db_model.User).get(user_id)


def get_user_by_name(db: Session, user_name: str) -> Optional[db_model.User]:
    try:
        return db.query(db_model.User).filter_by(name=user_name).one()
    except NoResultFound:
        return None


def create_user(db: Session, username: str, password: str, admin=False) -> db_model.User:
    inserted_user = db_model.User(name=username, password=get_password_hash(password), admin=admin)
    db.add(inserted_user)
    db.commit()
    db.refresh(inserted_user)
    return inserted_user


def _get_user_and_device(db: Session, user_id: int, device_id: int) -> Tuple[db_model.User, db_model.Device]:
    user: db_model.User = db.query(db_model.User).get(user_id)
    if not user:
        raise NotFoundException("user")
    device: db_model.Device = db.query(db_model.Device).get(device_id)
    if not device:
        raise NotFoundException("device")
    return user, device
