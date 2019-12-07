from typing import Optional, List

from sqlalchemy.orm import Session, Query, joinedload

import api.model.device as dto
from core.model import Device, User


def _query_single_device(db: Session, device_id: int, user: User) -> Query:
    query = db.query(Device).options(joinedload(Device.owners)).filter(Device.id == device_id)
    if not user.admin:
        query.join(Device.owners) \
            .filter(User.id == user.id)
    return query


def create_device(db: Session, device: dto.Device, user: User):
    db_device: Device = Device(**device.dict())
    db.add(db_device)
    db.flush()
    user.devices.append(db_device)
    db.commit()
    return db_device


def get_devices_of_user(db: Session, user: User) -> List[Device]:
    query = db.query(Device).options(joinedload(Device.owners))
    if not user.admin:
        query.join(Device.owners).filter(User.id == user.id)
    return query.all()


def get_device(db: Session, device_id: int, user: User) -> Optional[Device]:
    return _query_single_device(db, device_id, user).one()


def delete_device(db: Session, device_id: int, user: User):
    result = _query_single_device(db, device_id, user).delete()
    db.commit()
    return result


def update_device(db: Session, device_id: int, device: dto.Device, user: User) -> Optional[Device]:
    result = _query_single_device(db, device_id, user).update(device.dict())
    db.commit()
    if result:
        return get_device(db, device_id, user)
    return None
