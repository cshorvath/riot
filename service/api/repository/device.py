from typing import Optional, List, Tuple

from sqlalchemy.orm import Session, Query, joinedload

import api.model.device as dto
from core.model import Device, User


def _query_single_device(db: Session, device_id: int, user: User) -> Query:
    query = db.query(Device).options(joinedload(Device.source_rules)) \
        .filter(Device.id == device_id)
    if not user.admin:
        query.join(Device.owners) \
            .filter(User.id == user.id)
    return query


def create_device(db: Session, device: dto.Device, user: User):
    db_device: Device = Device(**device.dict())
    db.add(db_device)
    db.flush()
    user.devices.append(db_device)
    db.refresh(db_device)
    db.commit()
    return db_device


def get_devices_of_user(db: Session, user: User) -> List[Tuple[Device, int]]:
    query = db.query(Device).options(joinedload(Device.source_rules))
    if not user.admin:
        query.join(Device.owners).filter(User.id == user.id)
    devices = query.all()
    return [(device, len(device.source_rules)) for device in devices]


def get_device(db: Session, device_id: int, user: User) -> Tuple[Device, int]:
    device = _query_single_device(db, device_id, user).one()
    return device, len(device.source_rules)


def delete_device(db: Session, device_id: int, user: User):
    result = _query_single_device(db, device_id, user).delete()
    db.commit()
    return result


def update_device(db: Session, device_id: int, device: dto.Device, user: User) -> Optional[Tuple[Device, int]]:
    result = _query_single_device(db, device_id, user).update(device.dict())
    db.commit()
    if result:
        return get_device(db, device_id, user)
    return None
