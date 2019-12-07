from typing import Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import core.model as db_model
from api.model.user import NewUser
from api.util.auth import get_password_hash
from api.util.exception import NotFoundException


def get_all_users(db: Session):
    return db.query(db_model.User).all()


def get_user(db: Session, user_id: int) -> db_model.User:
    return db.query(db_model.User).get(user_id)


def change_password(db: Session, user_id: int, password: str) -> bool:
    result = db.query(db_model.User).filter_by(id=user_id).update({"password": get_password_hash(password)})
    db.commit()
    return bool(result)


def get_user_by_name(db: Session, user_name: str) -> Optional[db_model.User]:
    try:
        return db.query(db_model.User).filter_by(name=user_name).one()
    except NoResultFound:
        return None


def create_user(db: Session, user: NewUser) -> db_model.User:
    inserted_user = db_model.User(name=user.name, password=get_password_hash(user.password), admin=False)
    db.add(inserted_user)
    db.commit()
    db.refresh(inserted_user)
    return inserted_user


def delete_user(db: Session, user_id: int) -> bool:
    delete_count = db.query(db_model.User).filter_by(id=user_id).delete()
    db.commit()
    return delete_count


def _get_user_and_device(db: Session, user_id: int, device_id: int) -> Tuple[db_model.User, db_model.Device]:
    user: db_model.User = db.query(db_model.User).get(user_id)
    if not user:
        raise NotFoundException("user")
    device: db_model.Device = db.query(db_model.Device).get(device_id)
    if not device:
        raise NotFoundException("device")
    return user, device


def add_device_to_user(db: Session, user_id: int, device_id: int):
    user, device = _get_user_and_device(db, user_id, device_id)
    user.devices.append(device)
    db.commit()
    return user


def remove_device_from_user(db: Session, user_id: int, device_id: int):
    user, device = _get_user_and_device(db, user_id, device_id)
    user.devices.remove(device)
    db.commit()
    return user
