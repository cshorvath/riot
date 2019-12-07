from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

import api.model.device as dto
import api.repository.device as device_repository
from api.bootstrap import get_db
from core.model import User, Device

router = APIRouter()


@router.get("/", response_model=List[dto.DeviceResponse])
def get_owned_devices(db: Session = Depends(get_db)):
    return device_repository.get_devices(db, User(admin=True))


@router.post("/", response_model=dto.DeviceResponse)
def create_device(device: dto.Device, db: Session = Depends(get_db)):
    return device_repository.create_device(db, device, User(id=1))


@router.get("/{device_id}", response_model=dto.DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device: Optional[Device] = device_repository.get_device(db, device_id, User(id=1, admin=False))
    if not device:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return device


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    result = device_repository.delete_device(db, device_id, User(id=1, admin=True))
    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@router.patch("/{device_id}")
def update_device(device_id: int, device: dto.Device, db: Session = Depends(get_db)):
    result = device_repository.update_device(db, device_id, device, User(id=1, admin=True))
    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return result
