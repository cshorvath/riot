from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

import api.repository.user as user_repository
from api.bootstrap import get_db
from api.model.user import NewUser, User
from api.util.auth import admin_user, get_current_user

router = APIRouter()


@router.get("/", dependencies=[Depends(admin_user)], response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    return user_repository.get_all_users(db)


@router.post("/", response_model=User)
def create_user(user: NewUser, db: Session = Depends(get_db)):
    try:
        return user_repository.create_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="DUPLICATED_USER"
        )


@router.get("/me", response_model=User)
def get_current_user(user: User = Depends(get_current_user)):
    return user


@router.delete("/{user_id}", dependencies=[Depends(admin_user)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = user_repository.delete_user(db, user_id)
    if not result:
        raise HTTPException(HTTP_404_NOT_FOUND)


@router.put("/{user_id}/device/{device_id}", dependencies=[Depends(admin_user)])
def add_device_to_user(user_id: int, device_id: int, db: Session = Depends(get_db)):
    try:
        user_repository.add_device_to_user(db, user_id, device_id)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User or device does not exists"
        )
