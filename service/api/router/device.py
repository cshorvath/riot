from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

import api.model.device as dto
import api.repository.device as device_repository
from api.bootstrap import get_db
from api.util.auth import get_current_user, owner_user
from core.model import User

router = APIRouter()


@router.get("/", response_model=List[dto.DeviceResponse])
def get_owned_devices(db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    devices_with_rule_count_and_last_msg = device_repository.get_devices_of_user(db, user)
    return [dto.DeviceResponse(id=d.id, name=d.name, description=d.description, rule_count=r, last_message=l) for
            d, r, l in
            devices_with_rule_count_and_last_msg]


@router.post("/", response_model=dto.DeviceResponse)
def create_device(device: dto.Device,
                  user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    db_device = device_repository.create_device(db, device, user)
    return dto.DeviceResponse(id=db_device.id, name=db_device.name, description=db_device.description, rule_count=0)


@router.get("/{device_id}", response_model=dto.DeviceResponse)
def get_device(device_id: int,
               db: Session = Depends(get_db)):
    db_device, rule_count = device_repository.get_device(db, device_id)
    if not db_device:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return dto.DeviceResponse(id=db_device.id, name=db_device.name, description=db_device.description,
                              rule_count=rule_count)


@router.delete("/{device_id}", dependencies=[Depends(owner_user)])
def delete_device(device_id: int,
                  db: Session = Depends(get_db)):
    result = device_repository.delete_device(db, device_id)
    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@router.patch("/{device_id}", dependencies=[Depends(owner_user)])
def update_device(
        device_id: int,
        device: dto.Device,
        db: Session = Depends(get_db)):
    db_device, rule_count = device_repository.update_device(db, device_id, device)
    if not db_device:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return dto.DeviceResponse(id=db_device.id, name=db_device.name, description=db_device.description,
                              rule_count=rule_count)
