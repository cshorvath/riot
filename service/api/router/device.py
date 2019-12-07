from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

import api.model.device as dto
import api.repository.device as device_repository
from api.bootstrap import get_db
from api.util.auth import get_current_user
from core.model import User

router = APIRouter()


@router.get("/", response_model=List[dto.DeviceResponse])
def get_owned_devices(db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    devices_with_rule_count = device_repository.get_devices_of_user(db, user)
    return [dto.DeviceResponse(**d.__dict__, rule_count=r) for d, r in devices_with_rule_count]


@router.post("/", response_model=dto.DeviceResponse)
def create_device(device: dto.Device,
                  user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    return device_repository.create_device(db, device, user)


@router.get("/{device_id}", response_model=dto.DeviceResponse)
def get_device(device_id: int,
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    device, rule_count = device_repository.get_device(db, device_id, user)
    if not device:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return dto.DeviceResponse(**device.__dict__, rule_count=rule_count)


@router.delete("/{device_id}")
def delete_device(device_id: int,
                  user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    result = device_repository.delete_device(db, device_id, user)
    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@router.patch("/{device_id}")
def update_device(
        device_id: int,
        device: dto.Device,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    result = device_repository.update_device(db, device_id, device, user)
    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return result
