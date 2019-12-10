from typing import Optional, List, Tuple

from sqlalchemy.orm import Session, Query, joinedload
from sqlalchemy.orm.exc import NoResultFound

import api.model.device as dto
from api.util.exception import NotFoundException
from core.model import Device, User, user_device


def _query_single_device(db: Session, device_id: int) -> Query:
    query = db.query(Device).filter(Device.id == device_id)
    return query


def user_owns_device(db: Session, user_id: int, device_id: id) -> bool:
    return db.query(user_device).filter_by(user_id=user_id, device_id=device_id).count()


def create_device(db: Session, device: dto.Device, user: User):
    db_device: Device = Device(**device.dict())
    db.add(db_device)
    db.flush()
    user.devices.append(db_device)
    db.refresh(db_device)
    db.commit()
    return db_device


def get_devices_of_user(db: Session, user: User) -> List[Tuple[Device, int, int]]:
    query = db.query(Device)
    if not user.admin:
        query = query.join(Device.owners).filter(User.id == user.id)
    devices = query.all()
    return [(device, len(device.source_rules), len(device.messages)) for device in devices]


def get_device(db: Session, device_id: int) -> Tuple[Optional[Device], Optional[int]]:
    try:
        device = _query_single_device(db, device_id).one()
    except NoResultFound:
        return None, None
    rule_count = len(device.source_rules) if device else None
    return device, rule_count


def delete_device(db: Session, device_id: int):
    result = _query_single_device(db, device_id).delete()
    db.commit()
    return result


def update_device(db: Session, device_id: int, device: dto.Device) -> Optional[
    Tuple[Optional[Device], Optional[int]]]:
    result = _query_single_device(db, device_id).update(device.dict(exclude_unset=True))
    db.commit()
    if result:
        return get_device(db, device_id)
    return None, None
